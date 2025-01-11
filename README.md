HealthCheck App
![Health Check Logo](icon.png)
HealthCheck is a health monitoring web application designed to help users track their health metrics, manage their medical history, and gain insights into their health data. The app features user authentication, a powerful dashboard, and an intuitive UI/UX.

Table of Contents
Features

Technologies Used

Installation

Usage

Project Structure

Contributing

License

Contact

Features
1. User Authentication
Secure user registration and login.

Password hashing for enhanced security.

User profile management.

2. Dashboard
Edit Personal Info: Update username, email, and profile picture.

Medical History: Add, view, and remove diseases from your medical history.

Log Metrics: Track health metrics such as steps, water intake, sleep, calories, heart rate, blood pressure, and blood sugar.

Metrics Insights: View a detailed table of all logged metrics with timestamps.

3. UI/UX
Clean and modern design.

Responsive layout for seamless use on all devices.

Interactive buttons and animations for better user engagement.

Technologies Used
Backend
Flask: A lightweight Python web framework.

SQLAlchemy: ORM for database management.

Flask-Login: User session management.

Flask-Bcrypt: Password hashing.

SQLite: Database for development.

Frontend
HTML5: Structure of the web pages.

CSS3: Styling and animations.

JavaScript: Dynamic interactions and form handling.

Bootstrap: Responsive design and pre-built components.

Chart.js: For visualizing health metrics (if applicable).

Tools
Git: Version control.

VS Code: Code editor.

Postman: API testing.

Installation
Prerequisites
Python 3.8 or higher

pip (Python package manager)

Steps
Clone the Repository:

bash
Copy
git clone https://github.com/Mohamedalaagh/HealthCheck
cd HealthCheck
Set Up a Virtual Environment:

bash
Copy
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
Install Dependencies:

bash
Copy
pip install -r requirements.txt
Set Up the Database:

bash
Copy
flask shell
>>> db.create_all()
>>> exit()
Run the Application:

bash
Copy
flask run
Access the App:
Open your browser and go to http://127.0.0.1:5000.

Usage
Register: Create a new account.

Login: Access your dashboard.

Dashboard:

Edit your personal information.

Add or remove diseases from your medical history.

Log your daily health metrics.

View insights from your logged metrics.

Logout: Securely log out of your account.

Project Structure
Copy
HealthCheck/
├── package/
│   ├── __init__.py
│   ├── models.py
│   ├── routes.py
│   ├── forms.py
│   ├── templates/
│   │   ├── dashboard.html
│   │   ├── home.html
│   │   ├── login.html
│   │   ├── register.html
│   │   └── ...
│   └── static/
│       ├── css/
│       │   └── dashboard.css
│       ├── js/
│       │   ├── metrics.js
│       │   └── metrics-insights.js
│       └── images/
├── requirements.txt
├── app.py
└── README.md
Contributing
This project was developed individually due to unforeseen circumstances (mandatory military service). However, contributions are always welcome! If you'd like to contribute:

Fork the repository.

Create a new branch (git checkout -b feature/YourFeatureName).

Commit your changes (git commit -m 'Add some feature').

Push to the branch (git push origin feature/YourFeatureName).

Open a pull request.

License
This project is licensed under the MIT License. See the LICENSE file for details.

Contact
Mohamed Alaa
Email: mohamedalaaeid80@gmail.com

GitHub: https://github.com/Mohamedalaagh

Thank you for checking out HealthCheck! I hope this project demonstrates my backend development skills and ability to deliver a functional application under challenging circumstances. 🚀



