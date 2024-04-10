from flask import flash, redirect, render_template, Blueprint, url_for
from flask_login import current_user, login_required, login_user, logout_user
from app.Controller.auth_forms import (FacultyRegistrationForm, LoginForm, StudentRegistrationForm,)
from app.Model.models import Faculty, ResearchField, Student
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
            | (Student.email == sform.email.data)
        ).first()
        if existing_student:
            flash("Username or email is taken! Please try again.")
            return redirect(url_for("auth.register_student"))
        student = Student(
            username=sform.username.data,
            email=sform.email.data,
            firstname=sform.firstname.data,
            lastname=sform.lastname.data,
            major=sform.major.data,
            GPA=sform.gpa.data,
            graduationdate=sform.graduation_date.data,
            user_type="Student",
        )
        for topic in sform.topics_of_interest.data:
            student.topics_of_interest.append(topic)
        if sform.other_topics.data:
            other_topics = sform.other_topics.data.split(",")
            for topic in other_topics:
                newtopic = ResearchField(
                    id=ResearchField.query.count() + 1, title=topic
                )
                db.session.add(newtopic)
                student.topics_of_interest.append(newtopic)
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
            | (Student.email == fform.email.data)
        ).first()
        if existing_student:
            flash("Username or email is already registered as student.")
            return redirect(url_for("auth.register_faculty"))
        faculty = Faculty(username=fform.username.data)
        faculty = Faculty(
            username=fform.username.data,
            email=fform.email.data,
            firstname=fform.firstname.data,
            lastname=fform.lastname.data,
            user_type="Faculty",
        )
        for topic in fform.research_areas.data:
            faculty.research_areas.append(topic)
        if fform.other_topics.data:
            other_topics = fform.other_topics.data.split(", ")
            for topic in other_topics:
                newtopic = ResearchField(
                    id=ResearchField.query.count() + 1, title=topic
                )
                db.session.add(newtopic)
                faculty.research_areas.append(newtopic)
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
        route = "auth.login"
        if Student.query.filter_by(id=current_user.id).first():
            flash("Welcome, Student!")
            return redirect(url_for("routes.index"))
            # else check if user is a faculty
        elif Faculty.query.filter_by(id=current_user.id).first():
            flash("Welcome, Faculty!")
            return redirect(url_for("routes.index_faculty"))
        else:
            flash("Unknown user type")
            return redirect(url_for("auth.login"))

    lform = LoginForm()
    if lform.validate_on_submit():
        # check if user is a student, faculty, or if login fails
        faculty = Faculty.query.filter_by(username=lform.username.data).first()
        student = Student.query.filter_by(username=lform.username.data).first()
        if faculty and faculty.check_password(lform.password.data):
            login_user(faculty, remember=lform.remember_me.data)
            return redirect(url_for("routes.index"))
        elif student and student.check_password(lform.password.data):
            login_user(student, remember=lform.remember_me.data)
            return redirect(url_for("routes.index"))
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
