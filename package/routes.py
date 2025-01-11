from package.models import User
from flask import render_template, url_for, flash, redirect, request, jsonify, current_app
from package.forms import RegistrationForm, LoginForm, UpdateProfileForm
from package import app, bcrypt, db
from flask_login import login_user, current_user, logout_user, login_required
import os
from PIL import Image
import secrets
import json
from .models import MedicalHistory, HealthMetrics
from datetime import datetime

@app.route("/get-medical-history")
@login_required
def get_medical_history():
    medical_history = MedicalHistory.query.filter_by(user_id=current_user.id).all()
    history_data = [{
        "name": entry.disease_name,
        "type": entry.disease_type,
        "danger_percentage": entry.danger_percentage,
        "best_practices": entry.best_practices.split(', '),
        "link": entry.learn_more_link
    } for entry in medical_history]
    return jsonify(history_data)

@app.route("/save-medical-history", methods=["POST"])
@login_required
def save_medical_history():
    data = request.get_json()
    new_entry = MedicalHistory(
        user_id=current_user.id,
        disease_name=data.get('name'),
        disease_type=data.get('type'),
        danger_percentage=data.get('danger_percentage'),
        best_practices=', '.join(data.get('best_practices')),
        learn_more_link=data.get('link')
    )
    db.session.add(new_entry)
    db.session.commit()
    return jsonify({"message": "Disease added to medical history."})

@app.route("/remove-medical-history", methods=["POST"])
@login_required
def remove_medical_history():
    data = request.get_json()
    entry = MedicalHistory.query.filter_by(user_id=current_user.id, disease_name=data.get('name')).first()
    if entry:
        db.session.delete(entry)
        db.session.commit()
        return jsonify({"message": "Disease removed from medical history."})
    return jsonify({"error": "Disease not found in medical history."}), 404

@app.route('/')
@app.route("/home")
def home():
    return render_template('home.html', title="HealthCheck API")

@app.route("/register", methods=["GET", "POST"])
def register():
    if current_user.is_authenticated:
        return redirect(url_for("home"))
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_pass = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(fname=form.fname.data, lname=form.lname.data, username=form.username.data, email=form.email.data, password=hashed_pass)
        db.session.add(user)
        db.session.commit()
        flash(f"Account created successfully for {form.username.data}", "success")
        return redirect(url_for('login'))
    return render_template('register.html', title="register", form=form)

@app.route("/login", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for("home"))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            flash("You have been logged in!", "success")
            return redirect(url_for('home'))
        flash("Login Unsuccessful. Please check credentials", "danger")
    return render_template("login.html", title="Login", form=form)

@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for("home"))

@app.route("/dashboard", methods=["GET", "POST"])
@login_required
def dashboard():
    profile_form = UpdateProfileForm()
    if profile_form.validate_on_submit():
        if profile_form.image_file.data:
            picture_file = save_picture(profile_form.image_file.data)
            current_user.image_file = picture_file
        current_user.username = profile_form.username.data
        current_user.email = profile_form.email.data
        db.session.commit()
        flash("Your profile has been updated", "success")
        return redirect(url_for("dashboard"))
    elif request.method == "GET":
        profile_form.username.data = current_user.username
        profile_form.email.data = current_user.email
    with open(os.path.join(current_app.root_path, 'disease.json'), 'r') as file:
        disease_data = json.load(file)
    return render_template("dashboard.html", title="Dashboard", profile_form=profile_form, disease_data=disease_data)
