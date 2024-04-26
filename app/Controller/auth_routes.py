from flask import flash, redirect, render_template, Blueprint, session, url_for
from flask_login import current_user, login_required, login_user, logout_user
from app.Controller.auth_forms import (
    FacultyRegistrationForm,
    LoginForm,
    StudentRegistrationForm,
)
from app.Model.models import Faculty, ProgrammingLanguage, ResearchField, Student, User
from sqlalchemy import func
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
            major=sform.major.data.id,
            GPA=sform.gpa.data,
            graduationdate=sform.graduation_date.data,
            phone_number=sform.phone_number.data,
            user_type="Student",
        )
        for topic in sform.topics_of_interest.data:
            student.topics_of_interest.append(topic)
        if sform.other_topics.data:
            other_topics = sform.other_topics.data.split(",")
            for topic in other_topics:
                newtopic = ResearchField(
                    title=topic,
                )
                db.session.add(newtopic)
                db.session.commit()
                student.topics_of_interest.append(newtopic)
        for language in sform.languages.data:
            student.languages.append(language)
        if sform.other_languages.data:
            other_languages = sform.other_languages.data.split(",")
            for language in other_languages:
                newLanguage = ProgrammingLanguage(title=language)
                db.session.add(newLanguage)
                db.session.commit()
                student.languages.append(newLanguage)
        student.set_password(sform.password.data)
        db.session.add(student)
        db.session.commit()
        flash("You have successfully registered as a student!")
        login_user(student)
        return redirect(url_for("routes.index"))
    return render_template("register_student.html", form=sform)


@auth_blueprint.route("/register/faculty", methods=["GET", "POST"])
def register_faculty():
    fform = FacultyRegistrationForm()
    if fform.validate_on_submit():
        # Check if the username or email already exists in Student table
        existing_user = User.query.filter(
            (User.username == fform.username.data) | (User.email == fform.email.data)
        ).first()
        if existing_user:
            flash("Username or email is already registered.")
            return redirect(url_for("auth.register_faculty", form=fform))
        faculty = Faculty(username=fform.username.data)
        faculty = Faculty(
            username=fform.username.data,
            email=fform.email.data,
            firstname=fform.firstname.data,
            lastname=fform.lastname.data,
            department=fform.department.data.name,
            phone_number=fform.phone_number.data,
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
                db.session.commit()
                faculty.research_areas.append(newtopic)
        faculty.set_password(fform.password.data)
        db.session.add(faculty)
        db.session.commit()
        flash("You have successfully registered as faculty!")
        login_user(faculty)
        return redirect(url_for("routes.index"))
    return render_template("register_faculty.html", form=fform)


@auth_blueprint.route("/login", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        # check if user is a valid member
        if Student.query.filter_by(id=current_user.id).first() or Faculty.query.filter_by(id=current_user.id).first():
            flash("Welcome, " + current_user.firstname + "!")
            return redirect(url_for("routes.index"))
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
            flash("Welcome, " + current_user.firstname + "!")
            return redirect(url_for("routes.index"))
        elif student and student.check_password(lform.password.data):
            login_user(student, remember=lform.remember_me.data)
            flash("Welcome, " + current_user.firstname + "!")
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
