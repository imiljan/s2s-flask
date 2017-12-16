import os

basedir = os.path.dirname(__file__) # vraca dir ovog fajla

SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'app.db')  # gde ce se baza nalaziti
SQLALCHEMY_ECHO = True
SQLALCHEMY_TRACK_MODIFICATIONS = True

SECRET_KEY = 'nekaTajna...545+4645+1sdgaasdas54684+61+61+6'