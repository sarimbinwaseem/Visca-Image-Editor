from flask import Flask, request, render_template, redirect
from flask_sqlalchemy import SQLAlchemy
from config import Config
import os
from flask_migrate import Migrate


app = Flask(__name__)
app.config.from_object(Config)
db = SQLAlchemy(app)

@app.route("/auth", methods = ["POST"])
def auth():
    # git id pass from request and mathc it with the username and password in DB.
    username = request.form.get("username")
    password = request.form.get("pass")

    person = User.query.filter_by(username = username).first()
    if person is None:
        return "acnf" # account not found
    else:
        if password == person.password:
            return "alwd" # allowed

    return "0"

class User(db.Model):
    _id = db.Column("id", db.Integer, primary_key=True)
    username = db.Column("username", db.String(20), unique=True, nullable=False)
    password = db.Column("password", db.String(30), nullable=False)

    def __repr__(self):
        return f"User(\"{self.username}\" : \"{self.password}\")"

if __name__ == "__main__":
    db.create_all()
    app.run("0.0.0.0", port = 5656, debug = True)
