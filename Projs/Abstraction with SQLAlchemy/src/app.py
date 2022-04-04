from isort import code
from db import Assignment, db
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

    courses = [course.serialize() for course in Course.query.all()]
    return response(res=courses, success=True, code=200)
    

@app.route("/api/courses/", methods=["POST"])
def add_course():
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

    return response(res=course.serialize(), success=True, code=201)

@app.route("/api/courses/<int:course_id>/", methods=["GET"])
def get_course(course_id):
    course = Course.query.filter_by(id=course_id).first()

    if course: return response(res=course.serialize(), success=True, code=200)
    return response(res="No such course found", success=False, code=404)





# Added for testing purposes
@app.route("/api/drop/", methods=["POST"])
def drop_table():
    db.drop_all(bind=None)



if __name__ == "__main__":
    app.run(host="0.0.0.0", port=4000, debug=True)











if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
