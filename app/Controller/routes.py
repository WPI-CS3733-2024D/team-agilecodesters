from datetime import datetime
from flask import Blueprint
from flask import render_template, flash, redirect, url_for, request
from flask_login import login_required, current_user
from app.Controller.forms import (
    ApplicationForm,
    EditFacultyProfileForm,
    EditStudentProfileForm,
    CreatePositionForm,
    FacultySearchForm,
    EditPositionForm,
    StudentSearchForm,
)
from app.Model.models import (
    Applications,
    Faculty,
    PositionField,
    ProgrammingLanguage,
    ResearchField,
    ResearchPosition,
    Student,
)
from config import Config
from app import db
from app.Model.models import User

routes_blueprint = Blueprint("routes", __name__)
routes_blueprint.template_folder = Config.TEMPLATE_FOLDER


@routes_blueprint.route("/", methods=["GET", "POST"])
@routes_blueprint.route("/index", methods=["GET", "POST"])
@login_required
def index():
    # add logic to filter out research positions based on searches.
    # research positions that align with student queried information [search feature] will show on the screen.
    if current_user.user_type == "Student":
        search_form = StudentSearchForm()
    else:
        search_form = FacultySearchForm()
    posts = ResearchPosition.query.order_by(ResearchPosition.startDate.desc())

    if search_form.validate_on_submit():
        sort_option = search_form.sortOrder.data

        if sort_option == "Date":
            posts = ResearchPosition.query.order_by(ResearchPosition.startDate.asc())
        elif sort_option == "GPA":
            posts = ResearchPosition.query.order_by(ResearchPosition.wantedGPA.desc())
        elif current_user.user_type == "Student":
            if sort_option == "Recommended":

                def sortList(positions):
                    """
                    Sorts the position list based on topic and language scores
                    """
                    # Lists to hold positions based on scores
                    both_scores_higher = []
                    one_score_zero = []
                    both_scores_zero = []
                    above_user_gpa = []

                    # Iterate through positions and categorize based on scores and GPA
                    for pos in positions:
                        pos_topic_score = pos.topic_scorer(
                            current_user.topics_of_interest.all()
                        )
                        pos_language_score = pos.language_scorer(
                            current_user.languages.all()
                        )

                        # Check if required GPA is higher than user's GPA
                        if pos.wantedGPA > current_user.GPA:
                            above_user_gpa.append(pos)
                        else:
                            # Check other scores too
                            if pos_topic_score > 0 and pos_language_score > 0:
                                both_scores_higher.append(
                                    (pos, pos_topic_score + pos_language_score)
                                )
                                pos.recommended = True
                            elif (pos_topic_score > 0 and pos_language_score == 0) or (
                                pos_topic_score == 0 and pos_language_score > 0
                            ):
                                one_score_zero.append(
                                    (pos, pos_topic_score + pos_language_score)
                                )
                            else:
                                both_scores_zero.append(
                                    (pos, pos_topic_score + pos_language_score)
                                )

                    # Sort the lists based on combined scores
                    both_scores_higher.sort(key=lambda x: x[1], reverse=True)
                    one_score_zero.sort(key=lambda x: x[1], reverse=True)
                    both_scores_zero.sort(key=lambda x: x[1], reverse=True)

                    # Combine lists
                    sorted_positions = (
                        [pos[0] for pos in both_scores_higher]
                        + [pos[0] for pos in one_score_zero]
                        + [pos[0] for pos in both_scores_zero]
                        + above_user_gpa
                    )

                    return sorted_positions

                # Query and sort research positions based on relevancy score
                positions = ResearchPosition.query.all()
                posts = sortList(positions)

            elif sort_option == "Languages":
                shared_positions = ResearchPosition.query.filter(
                    ResearchPosition.languages.in_(
                        [lang.title for lang in current_user.languages]
                    )
                ).all()
                posts = shared_positions

            else:
                if sort_option == "Mine":
                    posts = ResearchPosition.query.filter_by(faculty=current_user.id)
                else:
                    posts = ResearchPosition.query.filter_by(faculty=current_user.id)

    return render_template(
        "index.html",
        title="Home",
        posts=posts,
        search_form=search_form,
        get_faculty=lambda id: Faculty.query.get(id),
    )


@routes_blueprint.route("/create_position", methods=["GET", "POST"])
@login_required
def create_position():
    if current_user.user_type != "Faculty":
        flash("You must be a faculty member to create a position!")
        return redirect(url_for("routes.index"))
    form = CreatePositionForm()
    if form.validate_on_submit():
        topics = []
        for topic in form.researchGoals.data:
            topics.append(topic)

        position = ResearchPosition(
            title=form.title.data,
            wantedGPA=form.wantedGPA.data,
            description=form.description.data,
            researchGoals=topics.__repr__(),
            startDate=form.startDate.data,
            endDate=form.endDate.data,
            timeCommitment=form.timeCommitment.data,
            languages=form.languages.data,
        )
        position.faculty = current_user.id
        db.session.add(position)
        db.session.commit()
        flash("Position created successfully!")
        return redirect(url_for("routes.index"))
    return render_template("_create-position.html", title="Create Position", form=form)


@routes_blueprint.route("/apply/<position_id>", methods=["POST"])
@login_required
def apply_for_position(position_id):
    if current_user.user_type != "Student":
        flash("You must be a student to apply for a position!")
        return redirect(url_for("routes.index"))
    position = ResearchPosition.query.get(position_id)
    aform = ApplicationForm()
    aform.firstname.data = current_user.firstname
    aform.lastname.data = current_user.lastname
    if aform.validate_on_submit() and request.method == "POST":
        existing_application = Applications.query.filter_by(
            studentID=current_user.id, position=position_id
        ).first()
        if existing_application:
            flash("You have already applied to this position!")
            return redirect(url_for("routes.index"))
        else:
            application = Applications(
                studentID=current_user.id,
                position=position_id,
                statement_of_interest=aform.statement_of_interest.data,
                referenceName=aform.reference_faculty_firstname.data
                + " "
                + aform.reference_faculty_lastname.data,
                referenceEmail=aform.reference_faculty_email.data,
            )
            db.session.add(application)
            db.session.commit()
            flash("Application submitted successfully!")
            return redirect(url_for("routes.index"))

    return render_template(
        "_apply.html",
        form=aform,
        position_id=position_id,
        position_title=position.title,
    )


@routes_blueprint.route("/unapply/<position_id>", methods=["POST"])
@login_required
def unapply_for_position(position_id):
    application = Applications.query.filter_by(
        studentID=current_user.id, position=position_id
    ).first()
    if application:
        db.session.delete(application)
        db.session.commit()
        flash("Successfully unapplied for the position.")
    return redirect(url_for("routes.view_applied"))


@routes_blueprint.route("/position/<position_id>", methods=["GET", "POST"])
@login_required
def view_position(position_id):
    position = ResearchPosition.query.get(position_id)
    return render_template(
        "view_position.html",
        title="Profile",
        position=position,
        get_faculty=lambda id: Faculty.query.get(id),
    )


@routes_blueprint.route("/position/edit/<position_id>", methods=["GET", "POST"])
@login_required
def edit_position(position_id):
    if (
        current_user.user_type != "Faculty"
        and current_user.id != ResearchPosition.query.get(position_id).faculty
    ):
        flash("You must be the faculty member who created this position to edit it!")
        return redirect(url_for("routes.index"))
    position = ResearchPosition.query.get(position_id)
    form = EditPositionForm()
    if form.validate_on_submit():
        position.title = form.title.data
        position.description = form.description.data
        if form.researchGoals.data:
            researchGoals = form.researchGoals.data.split(",")
            for goal in researchGoals:
                newGoal = PositionField(id=PositionField.query.count() + 1, title=goal)
                db.session.add(newGoal)
                db.session.commit()
                position.fields.append(newGoal)
        position.wantedGPA = form.wantedGPA.data
        position.languages = form.languages.data
        position.timeCommitment = form.timeCommitment.data
        position.startDate = form.startDate.data
        position.endDate = form.endDate.data
        db.session.add(position)
        db.session.commit()
        flash("Position updated successfully!")
        return redirect(url_for("routes.view_position", position_id=position_id))
    else:
        form.title.data = position.title
        form.description.data = position.description
        form.wantedGPA.data = position.wantedGPA
        form.languages.data = position.languages
        form.timeCommitment.data = position.timeCommitment
        form.startDate.data = position.startDate
        form.endDate.data = position.endDate
    return render_template(
        "edit_position.html", title="Edit Position", form=form, position=position
    )


@routes_blueprint.route("/position/delete/<position_id>", methods=["GET", "POST"])
@login_required
def delete_position(position_id):
    position = ResearchPosition.query.get(position_id)
    db.session.delete(position)
    db.session.commit()
    flash("Position deleted successfully!")
    return redirect(url_for("routes.view_created"))


@routes_blueprint.route("/profile", methods=["GET"])
@login_required
def view_profile():
    if current_user.user_type == "Faculty":
        posts = ResearchPosition.query.filter_by(faculty=current_user.id).all()
        return render_template(
            "profile.html",
            title="Profile",
            posts=posts,
            get_faculty=lambda id: Faculty.query.get(id),
        )
    else:
        return render_template("profile.html", title="Profile")


@routes_blueprint.route("/profile/edit", methods=["GET", "POST"])
@login_required
def edit_profile():
    if current_user.user_type == "Student":
        form = EditStudentProfileForm()
    else:
        form = EditFacultyProfileForm()
    if request.method == "POST":
        current_user.firstname = form.firstname.data
        current_user.lastname = form.lastname.data
        current_user.phone_number = form.phone_number.data
        current_user.email = form.email.data
        current_user.set_password(form.password.data)
        if current_user.user_type == "Faculty":
            current_user.research_areas = []
            current_user.department = form.department.data
            for topic in form.research_areas.data:
                current_user.research_areas.append(topic)
            if form.other_areas.data:
                other_areas = form.other_areas.data.split(",")
                for area in other_areas:
                    newArea = ResearchField(
                        id=ResearchField.query.count() + 1, title=area
                    )
                    db.session.add(newArea)
                    db.session.commit()
                    current_user.research_areas.append(newArea)
        if current_user.user_type == "Student":
            current_user.major = form.major.data
            current_user.GPA = form.GPA.data
            current_user.graduationdate = form.graduationdate.data
            current_user.topics_of_interest = []
            for topic in form.topics_of_interest.data:
                current_user.topics_of_interest.append(topic)
            if form.other_topics.data:
                other_topics = form.other_topics.data.split(",")
                for topic in other_topics:
                    newtopic = ResearchField(
                        id=ResearchField.query.count() + 1, title=topic
                    )
                    db.session.add(newtopic)
                    db.session.commit()
                    current_user.topics_of_interest.append(newtopic)
            current_user.languages = []
            for lang in form.languages.data:
                current_user.languages.append(lang)
            if form.other_languages.data:
                other_languages = form.other_languages.data.split(",")
                for language in other_languages:
                    newLanguage = ProgrammingLanguage(title=language)
                    db.session.add(newLanguage)
                    db.session.commit()
                    current_user.languages.append(newLanguage)

        db.session.add(current_user)
        db.session.commit()
        flash("Your profile has been updated!")
        return redirect(url_for("routes.view_profile"))
    elif request.method == "GET":
        form.firstname.data = current_user.firstname
        form.lastname.data = current_user.lastname
        form.phone_number.data = current_user.phone_number
        form.email.data = current_user.email
        if current_user.user_type == "Faculty":
            form.department.data = current_user.department
            form.research_areas.data = [
                topic.id for topic in current_user.research_areas
            ]
        if current_user.user_type == "Student":
            form.major.data = current_user.major
            form.GPA.data = current_user.GPA
            form.graduationdate.data = datetime.strptime(
                current_user.graduationdate.strftime("%Y-%m-%d"), "%Y-%m-%d"
            ).date()
            form.topics_of_interest.data = [
                topic.id for topic in current_user.topics_of_interest
            ]
    return render_template("edit_profile.html", title="Edit Profile", form=form)


@routes_blueprint.route("/profile/positions", methods=["GET", "POST"])
@login_required
def view_applied():
    if current_user.user_type != "Student":
        flash("Only students can view their applied positions!")
        return redirect(url_for("routes.index"))
    applications = Applications.query.filter_by(studentID=current_user.id).all()
    return render_template(
        "view_applied.html",
        title="Applied Positions",
        applications=applications,
        get_faculty=lambda id: User.query.get(id),
    )


@routes_blueprint.route("/profile/created", methods=["GET", "POST"])
@login_required
def view_created():
    if current_user.user_type != "Faculty":
        flash("Only faculty can view their created positions!")
        return redirect(url_for("routes.index"))
    positions = ResearchPosition.query.filter_by(faculty=current_user.id).all()
    return render_template(
        "view_created.html", title="Your Positions", positions=positions
    )


@routes_blueprint.route("/review_applications/<position_id>")
@login_required
def review_applications(position_id):
    if current_user.user_type != "Faculty":
        flash("Only faculty can review applications!")
        return redirect(url_for("routes.index"))
    position = ResearchPosition.query.get(position_id)
    applications = Applications.query.filter_by(position=position_id).all()
    return render_template(
        "review_applications.html", position=position, applications=applications
    )


@routes_blueprint.route("/accept_application/<position_id>/<studentID>", methods=["POST"])
@login_required
def accept_application(position_id, studentID):
    application = Applications.query.filter_by(position=position_id, studentID=studentID).first()
    application.status = "Approved for Interview"
    db.session.commit()
    flash("Application accepted successfully!")
    return redirect(url_for("routes.review_applications", position_id=position_id))


@routes_blueprint.route("/reject_application/<position_id>/<studentID>", methods=["POST"])
@login_required
def reject_application(position_id, studentID):
    application = Applications.query.filter_by(position=position_id, studentID=studentID).first()
    application.status = "Rejected"
    db.session.commit()
    flash("Application rejected successfully!")
    return redirect(url_for("routes.review_applications", position_id=position_id))


@routes_blueprint.route("/aboutus")
def about_us():
    return render_template("about_us.html", title="About Us")


@routes_blueprint.route("/profile/<user_id>")
def other_profile(user_id):
    student = Student.query.get(user_id)
    faculty = Faculty.query.get(user_id)

    if student:
        if current_user.user_type != "Faculty":
            flash("Only student profiles can be viewed from a faculty profile!")
            return redirect(url_for("routes.index"))
        else:
            return render_template("view_other_profile.html", user=student)
    elif faculty:
        posts = ResearchPosition.query.filter_by(faculty=faculty.id).all()
        return render_template(
            "view_other_profile.html",
            user=faculty,
            posts=posts,
            get_faculty=lambda id: Faculty.query.get(id),
        )
    return redirect(url_for("routes.index"))
