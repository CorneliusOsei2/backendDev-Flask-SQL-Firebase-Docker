from isort import code
from db import User, db
from flask import Flask, request
from db import Course
import json

app = Flask(__name__)
db_filename = "cms.db"

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///%s" % db_filename
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SQLALCHEMY_ECHO"] = True

db.init_app(app)
with app.app_context():
    db.create_all()

# Response Handler
def response(res={}, success = True, code = 200):
    if success: return json.dumps(res), code
    return json.dumps({"error": res}), code

# your routes here
@app.route("/api/courses/", methods=["GET"])
def get_courses():
    '''
    Get all courses
    '''
    courses = [course.serialize_for_course() for course in Course.query.all()]
    return response(res=courses, success=True, code=200)
    

@app.route("/api/courses/", methods=["POST"])
def add_course():
    '''
    Add new course
    '''
    body = json.loads(request.data)
    code = body.get("code", None)
    name = body.get("name", None)

    if code == None or body == None:
        return response("code and name fields required", False, 400)

    course = Course(
        code = code,
        name = name
    )

    db.session.add(course)
    db.session.commit()

    return response(res=course.serialize_for_course(), success=True, code=201)


@app.route("/api/courses/<int:course_id>/", methods=["GET"])
def get_course(course_id):
    '''
    Get course with id <course_id>
    '''
    course = Course.query.filter_by(id=course_id).first()

    if not course: return response(res="No such course found", success=False, code=404)
    return response(res=course.serialize_for_course(), success=True, code=200)


@app.route("/api/courses/<int:course_id>/", methods=["DELETE"])
def delete_course(course_id):
    '''
    Delete course with id <course_id>
    '''
    del_course = Course.query.filter_by(id=course_id).first()

    if not del_course: response(res="No such course found", success=False, code=404)

    db.session.delete(del_course)
    db.session.commit()
    return response(res=del_course.serialize_for_course(), success=True, code=200)

@app.route("/api/users/", methods=["GET"])
def get_users():
    '''
    Get all users
    '''
    users = [user.serialize_for_user() for user in User.query.all()]
    return response(res=users, success=True, code=200)

@app.route("/api/users/", methods=["POST"])
def create_user():
    '''
    Create a user
    '''
    body = json.loads(request.data)
    name, netid = body.get("name"), body.get("netid")

    if not name or not netid:
        return response(res="name and netid fields required", success=False, code=400)
    
    new_user = User(
        name = name,
        netid = netid
    )

    db.session.add(new_user)
    db.session.commit()

    return response(res=new_user.serialize_for_user(), success=True, code=201)

@app.route("/api/users/<int:user_id>/", methods=["GET"])
def get_user(user_id):
    '''
    Get user with id <user_id>
    '''
    user = User.query.filter_by(id=user_id).first()

    if not user: return response(res="No such user found!", success=False, code=404)
    return response(res=user.serialize_for_user(), success=True, code=200)


@app.route("/api/courses/<int:course_id>/add/", methods=["POST"])
def add_course_user(course_id):
    '''
    Add user to course with id <course_id>
    '''
    body = json.loads(request.data)
    user_id, role = body.get("user_id"), body.get("type")
    if (not user_id or not role) or not (role == "student" or role == "instructor"):
        return response(res="Valid user_id and type fields required!", success=False, code=400)

    user = User.query.filter_by(id=user_id).first()
    if not user: return response(res="No such user found!", success=False, code=404)
    course = Course.query.filter_by(id=course_id).first()
    if not course: return response(res="No such course found!", success=False, code=404)

    user.role = role
    course.users.append(user)
    db.session.commit()

    return response(res=course.serialize_for_course(), success=True, code=200)







# Added for testing purposes
@app.route("/api/drop/", methods=["POST"])
def drop_table():
    db.drop_all(bind=None)







 
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=4500, debug=True)
