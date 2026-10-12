from flask import Flask, request, render_template, redirect, url_for, session
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime, timedelta
from models import db, User, SOCAlert
import os
import socket
from concurrent.futures import ThreadPoolExecutor

app = Flask(__name__)
app.secret_key = "change-this-to-something-random-later"
app.permanent_session_lifetime = timedelta(days=7)

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///default.db"
app.config["SQLALCHEMY_BINDS"] = {
    "users_db": "sqlite:///users.db",
    "alerts_db": "sqlite:///alerts.db",
}
db.init_app(app)

# Logs failed login attempts for the SOC to detect
def log_failed_login(username, ip_address):
    os.makedirs("logs", exist_ok=True)
    timestamp = datetime.now().strftime("%b %d %H:%M:%S")
    log_line = f"{timestamp} webserver sshd[0000]: Failed password for invalid user {username} from {ip_address} port 0 ssh2\n"

    with open("logs/auth.log", "a") as f:
        f.write(log_line)


# Scanning Ports
def scan_port(target, port):
    """Checks a single port on the target. Returns the port number if open, else None."""
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.settimeout(0.5)
    result = sock.connect_ex((target, port))
    sock.close()
    return port if result == 0 else None


def run_scan(target, ports_to_scan):
    """Scans all given ports using multithreading, returns a sorted list of open ports."""
    open_ports = []
    with ThreadPoolExecutor(max_workers=200) as executor:
        results = executor.map(lambda p: scan_port(target, p), ports_to_scan)
        for result in results:
            if result is not None:
                open_ports.append(result)
    return sorted(open_ports)


# Checks if an IP has failed too many times recently -> triggers a SOC alert
def check_brute_force(ip_address, threshold=5):
    if not os.path.exists("logs/auth.log"):
        return

    with open("logs/auth.log") as f:
        lines = f.readlines()

    recent_failures = [line for line in lines[-20:] if f"from {ip_address}" in line]

    if len(recent_failures) >= threshold:
        new_alert = SOCAlert(
            time=datetime.now().strftime("%d %b %Y, %H:%M:%S"),
            ip=ip_address,
            message=f"Brute force detected — {len(recent_failures)} failed login attempts",
        )
        db.session.add(new_alert)
        db.session.commit()
        print(f"[MINI SOC ALERT] {new_alert.message} from {new_alert.ip}")


# Sign-up Page
@app.route("/signup", methods=["GET", "POST"])
def signup():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")

        existing_user = User.query.filter_by(username=username).first()
        if existing_user:
            return render_template(
                "signup.html",
                message="Username already exists. Try logging in instead.",
            )

        new_user = User(username=username, password_hash=generate_password_hash(password))
        db.session.add(new_user)
        db.session.commit()

        return render_template(
            "signup.html",
            message=f"Account created for {username}! You can now log in.",
        )

    return render_template("signup.html")


# Login Page
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")

        user = User.query.filter_by(username=username).first()

        if user and check_password_hash(user.password_hash, password):
            remember = request.form.get("remember")
            session.permanent = True if remember == "on" else False
            session["username"] = username
            return redirect(url_for("dashboard"))
        else:
            log_failed_login(username, request.remote_addr)
            check_brute_force(request.remote_addr)
            return render_template(
                "login.html", message="Invalid username or password."
            )

    return render_template("login.html")


# Scanner Dashboard
@app.route("/dashboard", methods=["GET", "POST"])
def dashboard():
    if "username" not in session:
        return redirect(url_for("login"))

    open_ports = None

    if request.method == "POST":
        target = request.form.get("target")
        consent = request.form.get("consent")
        port_input = request.form.get("ports")

        if consent != "on":
            return render_template(
                "dashboard.html",
                message="You must confirm authorization before scanning.",
            )

        try:
            if "-" in port_input:
                start_port, end_port = port_input.split("-")
                ports_to_scan = range(int(start_port.strip()), int(end_port.strip()) + 1)
            else:
                ports_to_scan = [int(p.strip()) for p in port_input.split(",")]
        except ValueError:
            return render_template(
                "dashboard.html",
                message="Invalid format. Use 22,80,443 for specific ports or 1-1024 for a range.",
            )

        open_ports = run_scan(target, ports_to_scan)

    return render_template("dashboard.html", open_ports=open_ports)


# SOC alerts dashboard
@app.route("/soc")
def soc_dashboard():
    if "username" not in session:
        return redirect(url_for("login"))

    all_alerts = SOCAlert.query.order_by(SOCAlert.id.desc()).all()
    return render_template("soc_dashboard.html", alerts=all_alerts)


# Home page -> redirect straight to signup
@app.route("/")
def home():
    return redirect(url_for("signup"))


with app.app_context():
    db.create_all()


if __name__ == "__main__":
    app.run(debug=True, port=5000)