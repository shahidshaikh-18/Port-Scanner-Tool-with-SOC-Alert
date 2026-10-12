# 🛡️ Port Scanner Tool with SOC Alert

A Python-based cybersecurity web application designed to scan network ports, identify potentially exposed services, and provide SOC-style security alerts through a web dashboard.

## 🚀 Features

- 🔎 **Port Scanning:** Identify open ports on authorized target systems.
- 📡 **Service Discovery:** Help identify potentially exposed network services.
- 🚨 **SOC Alerts:** Display security alerts and suspicious scan findings.
- 📊 **Security Dashboard:** View scanning results and security-related information.
- 🔐 **User Authentication:** Login and signup functionality.
- 📝 **Authentication Logs:** Maintain logs of relevant authentication events.
- 🗄️ **Database Integration:** Store application data and alerts in SQLite databases.
- 🎨 **Web Interface:** Dashboard built with HTML and CSS.

## 🛠️ Technology Stack

- **Language:** Python
- **Backend:** Flask
- **Frontend:** HTML, CSS
- **Database:** SQLite
- **ORM:** Flask-SQLAlchemy
- **Networking:** Python socket-based scanning or the scanning implementation in `port_scanner.py`
- **Security Monitoring:** SOC-style alert and logging functionality

## 📂 Project Structure

```text
Port-Scanner-Tool-With-SOC-Alert/
├── instance/
│   ├── alerts.db
│   ├── default.db
│   └── users.db
├── logs/
│   └── auth.log
├── static/
│   └── style.css
├── templates/
│   ├── dashboard.html
│   ├── login.html
│   ├── signup.html
│   └── soc_dashboard.html
├── app.py
├── models.py
├── port_scanner.py
├── requirements.txt
└── README.md
```

## ⚙️ Installation and Setup

### 1. Clone the repository

```bash
git clone https://github.com/YOUR-USERNAME/Port-Scanner-Tool-With-SOC-Alert.git
cd Port-Scanner-Tool-With-SOC-Alert
```

### 2. Create a virtual environment

**Windows PowerShell:**

```powershell
python -m venv venv
venv\Scripts\Activate.ps1
```

### 3. Install dependencies

```powershell
python -m pip install -r requirements.txt
```

### 4. Configure environment variables

Create a `.env` file containing the configuration required by your application. Never publish secret keys or database credentials.

### 5. Run the application

```powershell
python app.py
```

Open the local URL shown in the terminal.

## 🧪 Testing

- Scan systems you own or have explicit permission to test.
- Verify that open-port results are displayed correctly.
- Test login and signup validation.
- Confirm that relevant alerts appear in the SOC dashboard.
- Verify that authentication events are logged appropriately.
- Test database operations and error handling.

## 🔮 Future Enhancements

- Port and service risk classification.
- Real-time alert notifications.
- Exportable scan reports.
- Improved service fingerprinting.
- Alert severity levels and filtering.
- Scan history and audit trails.

## ⚠️ Disclaimer

This project is intended for educational cybersecurity practice and authorized network testing only. Do not scan systems without permission.

## 👨‍💻 Author

**Shahid Shaikh**

Aspiring Cybersecurity Analyst | VAPT & Penetration Testing Enthusiast
