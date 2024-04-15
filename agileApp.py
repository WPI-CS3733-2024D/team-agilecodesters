from config import Config
from app import create_app, db
from app.Model.models import Department, Major

app = create_app(Config)

@app.before_request
def initDB(*args, **kwargs):
    if app._got_first_request:
        db.create_all()
        if Department.query.count() == 0:
            departments = [
                {"name": "Computer Science"},
                {"name": "Engineering"},
                {"name": "Game ing"},
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
            for major in majors:
                with db.session.no_autoflush:
                    new_major = Major(name=major["name"], department=Department.query.filter_by(name=major["dname"]).first().id)
                    db.session.add(new_major)
            db.session.commit()



# will run only if this module is the 'main' module.
if __name__ == "__main__":
    app.run(debug=True)
