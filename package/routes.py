from package.models import User
from flask import render_template , url_for, flash, redirect, request , jsonify
from package.forms import RegistrationForm, LoginForm, UpdateProfileForm
from package import app, bcrypt, db
from flask_login import login_user , current_user, logout_user, login_required
import os
from flask import current_app
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
        "best_practices": entry.best_practices.split(', '),  # Convert string to list
        "link": entry.learn_more_link
    } for entry in medical_history]
    return jsonify(history_data)

@app.route("/save-medical-history", methods=["POST"])
@login_required
def save_medical_history():
    data = request.get_json()
    disease_name = data.get('name')
    disease_type = data.get('type')
    danger_percentage = data.get('danger_percentage')
    best_practices = ', '.join(data.get('best_practices'))  # Convert list to string
    learn_more_link = data.get('link')

    # Save the disease to the user's medical history
    new_entry = MedicalHistory(
        user_id=current_user.id,
        disease_name=disease_name,
        disease_type=disease_type,
        danger_percentage=danger_percentage,
        best_practices=best_practices,
        learn_more_link=learn_more_link
    )
    db.session.add(new_entry)
    db.session.commit()

    return jsonify({"message": "Disease added to medical history."})


@app.route("/remove-medical-history", methods=["POST"])
@login_required
def remove_medical_history():
    data = request.get_json()
    disease_name = data.get('name')

    # Find and remove the disease from the user's medical history
    entry = MedicalHistory.query.filter_by(user_id=current_user.id, disease_name=disease_name).first()
    if entry:
        db.session.delete(entry)
        db.session.commit()
        return jsonify({"message": "Disease removed from medical history."})
    else:
        return jsonify({"error": "Disease not found in medical history."}), 404

@app.route('/')
@app.route("/home")
def home():
    return render_template('home.html', title="HealthCheck API")

@app.route("/register", methods = ["Get", "Post"])
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
    return render_template('register.html', title="register", form = form)

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
        else:
            flash("Login Unsuccessful. Please check credentials", "danger")
    return render_template("login.html", title="Login", form=form)

@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for("home"))


@app.route("/about")
def about():
    return render_template('about.html', title="About")


@app.route("/contact")
def contact():
    return render_template('contact.html', title="contact us")




def save_picture(form_picture):
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_picture.filename)
    picture_fn = random_hex + f_ext
    picture_path = os.path.join(current_app.root_path, 'static/user_pics', picture_fn)

    # Resize the image (optional)
    output_size = (125, 125)
    img = Image.open(form_picture)
    img.thumbnail(output_size)
    img.save(picture_path)

    return picture_fn

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



@app.route("/update_info")
def update_info():
    return render_template('contact.html', title="contact us")


@app.route("/log-metrics", methods=["POST"])
@login_required
def log_metrics():
    data = request.form  # Get form data

    try:
        # Create a new HealthMetrics entry
        new_metrics = HealthMetrics(
            user_id=current_user.id,
            steps=int(data.get('steps')),
            water=float(data.get('water')),
            sleep=float(data.get('sleep')),
            calories=int(data.get('calories')),
            heart_rate=int(data.get('heart-rate')),
            blood_pressure=data.get('blood-pressure'),
            blood_sugar=int(data.get('blood-sugar')),
            timestamp=datetime.utcnow()  # Add a timestamp
        )
        db.session.add(new_metrics)
        db.session.commit()

        # Return a success message
        return jsonify({"message": "Metrics logged successfully!"}), 200

    except Exception as e:
        db.session.rollback()
        return jsonify({"error": f"Error: {str(e)}"}), 500

@app.route("/get-metrics")
@login_required
def get_metrics():
    metrics = HealthMetrics.query.filter_by(user_id=current_user.id).order_by(HealthMetrics.timestamp).all()
    labels = [m.timestamp.strftime('%Y-%m-%d %H:%M') for m in metrics]
    steps = [m.steps for m in metrics]
    return jsonify({"labels": labels, "steps": steps})



@app.route("/get-all-metrics", methods=["GET"])
@login_required
def get_all_metrics():
    # Fetch all metrics for the current user, ordered by timestamp
    all_metrics = HealthMetrics.query.filter_by(user_id=current_user.id).order_by(HealthMetrics.timestamp.desc()).all()

    if not all_metrics:
        return jsonify([])

    # Convert metrics to a list of dictionaries
    metrics_data = [{
        "timestamp": metric.timestamp.isoformat(),
        "steps": metric.steps,
        "water": metric.water,
        "sleep": metric.sleep,
        "calories": metric.calories,
        "heart_rate": metric.heart_rate,
        "blood_pressure": metric.blood_pressure,
        "blood_sugar": metric.blood_sugar
    } for metric in all_metrics]

    return jsonify(metrics_data)