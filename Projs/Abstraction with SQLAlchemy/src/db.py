from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

# your classes here
class Assignment(db.Model):
    __tablename__ = "assignments"
    id = db.Column(db.Integer, primary_key = True)
    course_id = db.Column(db.Integer, db.ForeignKey("courses.id"), nullable=False)

    def serialize(self):
        return {
            "id": self.id
        }


class User(db.Model):
    __tablename__ = "instructors"
    id = db.Column(db.Integer, primary_key = True)
    course_id = db.Column(db.Integer, db.ForeignKey("courses.id"), nullable=False)

    def serialize(self):
        return {
            "id": self.id
        }


class Course(db.Model):
    __tablename__ = "courses"
    id = db.Column(db.Integer, primary_key = True)
    code = db.Column(db.String, nullable = False)
    name = db.Column(db.String, nullable = False)
    assignments = db.relationship("Assignment", cascade="delete")
    instructors = db.relationship("User", cascade="delete")
    students = db.relationship("User", cascade="delete")


    def serialize(self):
        return {
            "id": self.id,
            "code": self.code,
            "name": self.name,
            "assignments": [assignment.serialize() for assignment in self.assignments],
            "instructors": [instructor.serialize() for instructor in self.instructors],
            "students": [student.serialize() for student in self.students]
        }
