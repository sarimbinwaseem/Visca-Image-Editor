from flask import Flask, request, render_template, redirect
from flask_sqlalchemy import SQLAlchemy
from config import Config
import os
from flask_migrate import Migrate


app = Flask(__name__)
app.config.from_object(Config)
db = SQLAlchemy(app)

@app.route("/auth", methods = ["GET"])
def auth():
    # git id pass from request and mathc it with the username and password in DB.
    pass

class User(db.Model):
    _id = db.Column("id", db.Integer, primary_key=True)
    username = db.Column("username", db.String(20), unique=True, nullable=False)
    password = db.Column("password", db.String(30), nullable=False)

    def __repr__(self):
        return f"User(\"{self.username}\" : \"{self.password}\")"

if __name__ == "__main__":
    db.create_all()
    app.run("0.0.0.0", port = 5656, debug = True)
