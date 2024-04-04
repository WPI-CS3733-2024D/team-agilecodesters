from config import Config
from app import create_app, db

app = create_app(Config)

@app.before_request
def initDB(*args, **kwargs):
    if app._got_first_request:
        db.create_all()


# will run only if this module is the 'main' module.
if __name__ == "__main__":
    app.run(debug=True)