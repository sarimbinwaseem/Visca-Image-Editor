import os

class Config:
    basedir = os.path.abspath(os.path.dirname(__file__))
    SECRET_KEY = "Thesecretkeyoftheultimatevisca"
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'database.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = True
