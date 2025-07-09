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

auth_blueprint = Blueprint("auth", __name__) # auth.[route_name] will be used to access routes in this file.
auth_blueprint.template_folder = Config.TEMPLATE_FOLDER # templates of blueprints are stored here.

# CONCEPT: This file allows use to do operations with the data collected from the authentication forms.

@auth_blueprint.route("/register/student", methods=["GET", "POST"])
def register_student():
    sform = StudentRegistrationForm()
    if sform.validate_on_submit():
        # Check if the username or email already exists in Faculty table
        existing_student = Student.query.filter(
            (Student.username == sform.username.data)
            | (Student.email == sform.email.data)
        ).first()

        # If the username already exists, this data cannot be registered.
        if existing_student:
            flash("Username or email is taken! Please try again.")
            return redirect(url_for("auth.register_student"))
        
        # If the username does not exist, then we can register the student.

        # we populate the student object with data from the form.
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

        # for each topic chosen in the form, we add it to student's topic of interest in database.
        for topic in sform.topics_of_interest.data:
            student.topics_of_interest.append(topic)

        # here is where we will handle the comma-separated topics of interest.
        if sform.other_topics.data:
            other_topics = sform.other_topics.data.split(",") # deliminate by comma

            # for each topic of interest, newtopic is created and added to the database.
            # every topic has to have a research field and each topic is the title of the research field.
            # non-included topics are just added as NEW research fields for the topic to the db.
            for topic in other_topics:
                newtopic = ResearchField(
                    title=topic,
                )
                db.session.add(newtopic)
                db.session.commit()
                student.topics_of_interest.append(newtopic)

        # for each language chosen in the form, we add it to the student's proficient languages.
        # 
        for language in sform.languages.data:
            student.languages.append(language)

        # comma separated languages are handled here.
        # every language is a programming language object with a title the name of the language.
        # each non-included language is added as a NEW programming language and commited to the database.
        if sform.other_languages.data:
            other_languages = sform.other_languages.data.split(",")
            for language in other_languages:
                newLanguage = ProgrammingLanguage(title=language)
                db.session.add(newLanguage)
                db.session.commit()
                student.languages.append(newLanguage)

        # set the password for the student with the data from the form. Commmit new created student object to database.
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
        existing_user = User.query.filter(
            (User.username == fform.username.data) | (User.email == fform.email.data)
        ).first()
        if existing_user:
            flash("Username or email is already registered.")
            return redirect(url_for("auth.register_faculty", form=fform))
        faculty = Faculty(username=fform.username.data)

        # populate database with data about faculty from form.
        faculty = Faculty(
            username=fform.username.data,
            email=fform.email.data,
            firstname=fform.firstname.data,
            lastname=fform.lastname.data,
            department=fform.department.data.name,
            phone_number=fform.phone_number.data,
            user_type="Faculty",
        )

        # for every topic picked in the form, we add it to the faculty's research areas.
        for topic in fform.research_areas.data:
            faculty.research_areas.append(topic)

        # here is where we handle the comma-separated research areas.
        # every topic is a research field object with a title the name of the research area.
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
        return redirect(url_for("auth.login"))
    return render_template("register_faculty.html", form=fform)


@auth_blueprint.route("/login", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        # check if user is a student or a faculty.
        route = "auth.login"

        # Checking the ID of the current user.
        # if the user is a student and we find them already registered then go to the 'main' index page.
        # if faculty is registered, then do the same thing.
        # else we don't know the user type, and they do not proceed.
        if Student.query.filter_by(id=current_user.id).first():
            flash("Welcome, Student!")
            return redirect(url_for("routes.index"))
            # else check if user is a faculty
        elif Faculty.query.filter_by(id=current_user.id).first():
            flash("Welcome, Faculty!")
            return redirect(url_for("routes.index"))
        else:
            flash("Unknown user type")
            return redirect(url_for("auth.login"))

    lform = LoginForm()
    if lform.validate_on_submit():
        # check if user is a student, faculty, or if login fails

        #Find faculty and student objects in the database with the username.
        faculty = Faculty.query.filter_by(username=lform.username.data).first()
        student = Student.query.filter_by(username=lform.username.data).first()

        # if the username and their password is exists/matches for that user, then login the user(either Faculty or student).
        # login_user() is a utils function we didn't implement.
        if faculty and faculty.check_password(lform.password.data):
            login_user(faculty, remember=lform.remember_me.data)
            return redirect(url_for("routes.index"))
        elif student and student.check_password(lform.password.data):
            login_user(student, remember=lform.remember_me.data)
            return redirect(url_for("routes.index"))
        else:
            # login failed. Username/password combination is invalid.
            flash("Invalid username or password")
            return redirect(url_for("auth.login"))
    return render_template("login.html", title="Sign in", form=lform)


@auth_blueprint.route("/logout", methods=["GET"])
@login_required # decorator ensures only logged in users can log out and be redirected to the login page.
def logout():
    # utils function we didn't implement.
    logout_user()
    return redirect(url_for("auth.login"))
