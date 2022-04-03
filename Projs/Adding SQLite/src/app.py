import json
from flask import Flask, request
import db

DB = db.DatabaseDriver()

app = Flask(__name__)


@app.route("/")
def hello_world():
    return "Hello world!"

# Response Handler
def response(res, success = True, code = 200):
    if success: return json.dumps(res), code
    return json.dumps({"error": res}), code


# Routes
@app.route("/api/users/", methods=["GET"])
def get_users():
    '''
        Get all users
    '''

    res = {"users": DB.get_users()}
    return response(res)

@app.route("/api/users/", methods=["POST"])
def create_user():
    '''
        Create a new user
    '''
    body = json.loads(request.data)

    if not (body.get("name") and body.get("username")):
        return response("user and username fields required!", False, 400)

    res = DB.create_user(
        body["name"], body["username"], body.get("balance", 0)
        )
    
    return response(res)


@app.route("/api/users/<int:user_id>/", methods=["GET"])
def get_user(user_id):
    '''
        Get user with id <user_id>
    '''

    user = DB.get_user(user_id)
    if user: return response(user)
    return response("No such user found!", False, 404)


@app.route("/api/users/<int:user_id>/", methods=["DELETE"])
def delete_user(user_id):
    '''
        Delete user with id <user_id>
    '''

    user = DB.delete_user(user_id)
    if user: return response(user)
    return response("No such user found!", False, 404)

@app.route("/api/send/", methods=["POST"])
def send():
    '''
        Send money from one user to another
    '''

    body = json.loads(request.data)
    sender = body.get("sender_id")
    receiver = body.get("receiver_id")
    amount = body.get("amount")

    if not (sender is not None and receiver is not None and
             amount is not None and amount >= 0):
        return response("sender_id, receiver_id and amount fields required", False, 400)

    res = DB.send(sender, receiver, amount)

    if res == True:
        return response(body)
    return response(res, False, 400)

# Added for testing purposes
@app.route("/api/delete/all/", methods=["DELETE"])
def delete_all():
    '''
        Delete all users.
    '''

    return response(DB.delete_all())


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=4000, debug=True)
