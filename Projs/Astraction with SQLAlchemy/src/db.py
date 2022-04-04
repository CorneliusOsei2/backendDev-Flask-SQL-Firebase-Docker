from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

# your classes here

class Course(db.Model):
    __tablename__ = "course"
    id = db.Column(db.Integer, primary_key = True)
    code = db.Column(db.String, nullable = False)
    name = db.Column(db.String, nullable = False)
    assignments = db.Column(db.ARRAY)
    instructors = db.Column(db.ARRAY)
    students = db.Column(db.ARRAY)