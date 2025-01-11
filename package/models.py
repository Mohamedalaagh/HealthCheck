from package import db, login_manager
from flask_login import UserMixin
from datetime import datetime


# User loader for Flask-Login
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# User Table (Main Database)
class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    fname = db.Column(db.String(25), nullable=False)
    lname = db.Column(db.String(25), nullable=False)
    username = db.Column(db.String(25), unique=True, nullable=False)
    email = db.Column(db.String(125), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)
    image_file = db.Column(db.String(20), nullable=False, default='default_image.png')
    medical_history = db.relationship('MedicalHistory', backref='user', lazy=True)  # Link to MedicalHistory

    def __repr__(self):
        return f"{self.fname}, {self.lname}, {self.username}, {self.email}"

# Medical History Table (Main Database)
class MedicalHistory(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)  # Foreign key to User
    disease_name = db.Column(db.String(100), nullable=False)
    disease_type = db.Column(db.String(50), nullable=False)
    danger_percentage = db.Column(db.Integer, nullable=False)
    best_practices = db.Column(db.String(500), nullable=False)
    learn_more_link = db.Column(db.String(200), nullable=False)

    def __repr__(self):
        return f"MedicalHistory(user_id={self.user_id}, disease_name={self.disease_name})"
    


class HealthMetrics(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    steps = db.Column(db.Integer, nullable=False)
    water = db.Column(db.Float, nullable=False)
    sleep = db.Column(db.Float, nullable=False)
    calories = db.Column(db.Integer, nullable=False)
    heart_rate = db.Column(db.Integer, nullable=False)
    blood_pressure = db.Column(db.String(20), nullable=False)
    blood_sugar = db.Column(db.Integer, nullable=False)
    timestamp = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    def __repr__(self):
        return f"HealthMetrics(user_id={self.user_id}, timestamp={self.timestamp})"