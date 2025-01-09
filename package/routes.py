from package.models import User
from flask import render_template , url_for, flash, redirect, request 
from package.forms import RegistrationForm, LoginForm, UpdateProfileForm
from package import app, bcrypt, db
from flask_login import login_user , current_user, logout_user, login_required

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


@app.route("/dashboard", methods=["GET", "POST"])
@login_required
def dashboard():
    profile_form = UpdateProfileForm()
    if profile_form.validate_on_submit():

        current_user.username = profile_form.username.data
        current_user.email = profile_form.email.data
        db.session.commit()
        flash("Your profile has been updated", "success")
        return redirect(url_for("dashboard"))
    elif request.method == "GET":
        profile_form.username.data = current_user.username
        profile_form.email.data = current_user.email
    return render_template(
        "dashboard.html",
        title="Dashboard",
        profile_form=profile_form,
    )



@app.route("/update_info")
def update_info():
    return render_template('contact.html', title="contact us")