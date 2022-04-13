from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

# Associations

# Many-to-many relationship between users and courses
users_courses_table = db.Table("users_courses", db.Model.metadata,
    db.Column("user_id", db.Integer, db.ForeignKey("users.id")),
    db.Column("course_id", db.Integer, db.ForeignKey("courses.id"))
)

# your classes here
class Assignment(db.Model):
    '''
    An instance is a row representing an assignment in an <assignments> table
    '''
    __tablename__ = "assignments"
    id = db.Column(db.Integer, primary_key = True)
    title = db.Column(db.String, nullable=False)
    due_date = db.Column(db.Integer, nullable=False)
    course_id = db.Column(db.Integer, db.ForeignKey("courses.id"))
    course = db.relationship("Course", cascade="delete")

    def serialize_for_assignment(self):
        return {
            "id": self.id,
            "title": self.title,
            "due_date": self.due_date,
            "course": {
                "id": self.course.id,
                "code": self.course.code,
                "name": self.course.name
            }
        }
    
    def serialize_for_course(self):
        return {
            "id": self.id,
            "title": self.title,
            "due_date": self.due_date
        }


class User(db.Model):
    '''
    An instance is a row representing a user in a <users> table
    '''

    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String, nullable=False)
    netid = db.Column(db.String, nullable=False)
    role = db.Column(db.String)
    courses = db.relationship("Course", secondary=users_courses_table, back_populates='users')
    
    def serialize_for_user(self):
        return {
            "id": self.id,
            "name": self.name,
            "netid": self.netid,
            "courses": [course.serialize_for_user() for course in self.courses]
        }
    
    def serialize_for_course(self):
        return {
            "id": self.id,
            "name": self.name,
            "netid": self.netid
        }


class Course(db.Model):
    '''
    An instance is a row representing a course in a <courses> table
    '''
    __tablename__ = "courses"
    id = db.Column(db.Integer, primary_key = True)
    code = db.Column(db.String, nullable = False)
    name = db.Column(db.String, nullable = False)
    users = db.relationship("User", secondary=users_courses_table, back_populates='courses')    #many-to-many-relationship
    assignments = db.relationship("Assignment", cascade="delete") #one-to-many relationship


    def serialize_for_course(self):
        return {
            "id": self.id,
            "code": self.code,
            "name": self.name,
            "assignments": [assignment.serialize_for_course() for assignment in self.assignments],
            "instructors": [user.serialize_for_course() for user in self.users if user.role == "instructor"],
            "students": [user.serialize_for_course() for user in self.users if user.role == "student"]
        }
    
    def serialize_for_user(self):
        return {
            "id": self.id,
            "code": self.code,
            "name": self.name
        }
