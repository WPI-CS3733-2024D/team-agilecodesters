from flask import flash, redirect, render_template, Blueprint, url_for
from flask_login import current_user, login_required, login_user, logout_user
from app.Controller.auth_forms import (
    FacultyRegistrationForm,
    LoginForm,
    StudentRegistrationForm,
)
from app.Model.models import Faculty, Student, User
from config import Config
from app import db

auth_blueprint = Blueprint("auth", __name__)
auth_blueprint.template_folder = Config.TEMPLATE_FOLDER


@auth_blueprint.route("/register/student", methods=["GET", "POST"])
def register_student():
    sform = StudentRegistrationForm()
    if sform.validate_on_submit():
        # Check if the username or email already exists in Faculty table
        existing_student = Student.query.filter(
            (Student.username == sform.username.data)
            #| (Student.email == sform.email.data)
        ).first()
        if existing_student:
            flash("Username or email is taken! Please try again.")
            return redirect(url_for("auth.register_student"))
        student = Student(username=sform.username.data)
        # student = Student(
        #     username=sform.username.data,
        #     email=sform.email.data,
        #     firstname=sform.firstname.data,
        #     lastname=sform.lastname.data,
        #     major=sform.major.data,
        #     GPA=sform.gpa.data,
        #     graduationdate=sform.graduation_date.data,
        #     topics_of_interest=sform.topics_of_interest.data, 
        #     user_type="Student")
        student.set_password(sform.password.data)
        db.session.add(student)
        db.session.commit()
        flash("You have successfully registered as a student!")
        return redirect(url_for("auth.login"))
    return render_template("register_student.html", form=sform)


@auth_blueprint.route("/register/faculty", methods=["GET", "POST"])
def register_faculty():
    fform = FacultyRegistrationForm()
    if fform.validate_on_submit():
        # Check if the username or email already exists in Student table
        existing_student = Student.query.filter(
            (Student.username == fform.username.data)
            #| (Student.email == fform.email.data)
        ).first()
        if existing_student:
            flash("Username or email is already registered as student.")
            return redirect(url_for("auth.register_faculty"))
        faculty = Faculty(username=fform.username.data)
        # faculty = Faculty(
        #     username=fform.username.data,
        #     email=fform.email.data,
        #     firstname=fform.firstname.data,
        #     astname=fform.lastname.data,
        #     research_areas=fform.research_areas.data,
        #     user_type='faculty')
        faculty.set_password(fform.password.data)
        db.session.add(faculty)
        db.session.commit()
        flash("You have successfully registered as faculty!")
        return redirect(url_for("auth.login"))
    return render_template("register_faculty.html", form=fform)


@auth_blueprint.route("/login", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        # check if user is a student
        if Student.query.filter_by(id=current_user.id).first():
            return redirect(url_for("routes.index_student"))
        # else check if user is a faculty
        elif Faculty.query.filter_by(id=current_user.id).first():
            return redirect(url_for("routes.index_faculty"))
        else:
            # TODO return some error
            return redirect(url_for("login.html"))
    lform = LoginForm()
    if lform.validate_on_submit():
        # check if user is a student, faculty, or if login fails
        if Faculty.query.filter_by(username=lform.username.data).first() is not None:
            faculty = Faculty.query.filter_by(username=lform.username.data).first()
            login_user(faculty, remember=lform.remember_me.data)
            return redirect(url_for("routes.index_faculty"))
        elif Student.query.filter_by(username=lform.username.data).first() is not None:
            student = Student.query.filter_by(username=lform.username.data).first()
            login_user(student, remember=lform.remember_me.data)
        else:
            # login failed
            flash("Invalid username or password")
            return redirect(url_for("auth.login"))
    return render_template("login.html", title="Sign in", form=lform)


@auth_blueprint.route("/logout", methods=["GET"])
@login_required
def logout():
    logout_user()
    return redirect(url_for("auth.login"))
