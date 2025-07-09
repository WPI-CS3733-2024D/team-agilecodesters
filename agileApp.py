from config import Config
from app import create_app, db
from app.Model.models import Department, Major, ProgrammingLanguage, ResearchField

app = create_app(Config)


@app.before_request
def initDB(*args, **kwargs):
    if app._got_first_request:
        db.create_all()
        if Department.query.count() == 0:
            departments = [
                {"name": "Computer Science"},
                {"name": "Engineering"},
                {"name": "Gaming"},
                {"name": "Business"},
                {"name": "Hard Sciences"},
            ]
            for department in departments:
                new_department = Department(name=department["name"])
                db.session.add(new_department)
            db.session.commit()
        if Major.query.count() == 0:
            majors = [
                {"name": "Computer Science", "dname": "Computer Science"},
                {"name": "Robotics Engineering", "dname": "Engineering"},
                {"name": "Electrical and Computer Engineering", "dname": "Engineering"},
                {"name": "Mechanical Engineering", "dname": "Engineering"},
                {"name": "Chemical Engineering", "dname": "Engineering"},
                {"name": "Game ing", "dname": "Game ing"},
                {"name": "Coloring", "dname": "Business"},
                {"name": "Biology", "dname": "Hard Sciences"},
                {"name": "Chemistry", "dname": "Hard Sciences"},
                {"name": "Biochemistry", "dname": "Hard Sciences"},
                {"name": "Physics", "dname": "Hard Sciences"},
                {"name": "Biochemicalphysics", "dname": "Hard Sciences"},
            ]

            # If there is a department, then there is a major.
            for major in majors:
                with db.session.no_autoflush:
                    department = Department.query.filter_by(name=major["dname"]).first()
                    if department:
                        new_major = Major(name=major["name"], department=department.id)
                        db.session.add(new_major)
            db.session.commit()

        if ProgrammingLanguage.query.count() == 0:
            languages = [
                "Python",
                "Java",
                "JavaScript",
                "C",
                "C++",
                "C#",
                "Ruby",
                "Swift",
                "Go",
                "PHP",
                "Kotlin",
            ]
            for lang in languages:
                new_lang = ProgrammingLanguage(title=lang)
                db.session.add(new_lang)
            db.session.commit()

        if ResearchField.query.count() == 0:
            fields = [
                "Artificial Intelligence",
                "Quantum Computing",
                "Machine Learning",
                "Ending the World",
                "Robotics",
                "Neural Networks",
                "Cybersecurity",
                "Biotechnology",
                "Space Exploration",
                "Becoming Iron Man",
                "Nanotechnology",
                "Augmented Reality",
                "Virtual Reality",
            ]
            for field in fields:
                new_field = ResearchField(title=field)
                db.session.add(new_field)
            db.session.commit()


# will run only if this module is the 'main' module.
if __name__ == "__main__":
    app.run(debug=True)
