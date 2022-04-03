import json
from flask import Flask, request
import db
from datetime import datetime as dt

DB = db.DatabaseDriver()

app = Flask(__name__)


@app.route("/")
def hello_world():
    return "Hello world!"

# Response Handler
def response(res={}, success = True, code = 200):
    if success: return json.dumps(res), code
    return json.dumps({"error": res}), code


# Routes
@app.route("/api/users/", methods=["GET"])
def get_users():
    '''
        Get all users
    '''

    res = {"users": DB.get_users()}
    return response(res=res, success=True, code=200)

@app.route("/api/users/", methods=["POST"])
def create_user():
    '''
        Create a new user
    '''

    body = json.loads(request.data)

    if not (body.get("name") and body.get("username")):
        return response(res="user and username fields required!", success=False, code=400)

    res = DB.create_user(
        body["name"], body["username"], body.get("balance", 0)
        )
    
    return response(res=res, success=True, code=201)


@app.route("/api/users/<int:user_id>/", methods=["GET"])
def get_user(user_id):
    '''
        Get user with id <user_id>
    '''

    user = DB.get_user(user_id)
    if user: return response(res=user, success=True, code=200)
    return response(res="No such user found!", success=False, code=404)


@app.route("/api/users/<int:user_id>/", methods=["DELETE"])
def delete_user(user_id):
    '''
        Delete user with id <user_id>
    '''

    user = DB.delete_user(user_id)
    print(user)
    if user: return response(res=user, success=True, code=200)
    return response(res="No such user found!", success=False, code=404)


@app.route("/api/transactions/")
def get_transactions():
    '''
        Get all transactions
    '''

    res = DB.get_transactions()
    return response(res=res, success=True, code=200)
  
@app.route("/api/transactions/", methods=["POST"])
def transact():
    '''
        Execute a transaction
    '''

    body = json.loads(request.data)
    sender = body.get("sender_id")
    receiver = body.get("receiver_id")
    amount = body.get("amount")
    message = body.get("message")
    accepted = body.get("accepted")

    if (sender is not None and receiver is not None and
             amount is not None and amount < 0 and message is not None and accepted is not None):
        return response("sender_id, receiver_id, amount, message and accepted fields required", False, 400)

    res = DB.exec_transactions(sender, receiver, amount, message, accepted)
    
    out = transactions_helper(res)
    return response(res=out, success=True, code=201)

    
@app.route("/api/transactions/<int:txn_id>/", methods=["POST"])
def accept_deny_transaction(txn_id):
    '''
        Respond to a transaction
    '''

    body = json.loads(request.data)
    accepted = body["accepted"]
    res = DB.update_transaction(accepted, txn_id)

    if "error" in res:
        return response(res["error"], False, res["code"])

    out = transactions_helper(res)
    return response(res=out, success=True, code=200)

def transactions_helper(res):
    '''
        Parse transaction
    '''
    if "error" in res:
        return response(res["error"], False, res["code"]) 

    out = {
        "id": res["id"],
        "timestamp": dt.now().strftime('%Y-%m-%d %H:%M:%S'),
        "sender_id": res["sender_id"],
        "receiver_id": res["receiver_id"],
        "amount": res["amount"],
        "message": res["message"],
        "accepted": res["accepted"]
    }

    return out
    

# Added for testing purposes
@app.route("/api/users/delete/all/", methods=["DELETE"])
def delete_all_users():
    '''
        Delete all users.
    '''
    return response(DB.delete_all_users())

# Added for testing purposes
@app.route("/api/transactions/delete/all/", methods=["DELETE"])
def delete_all_transactions():
    '''
        Delete all users.
    '''
    res = response(DB.delete_all_transactions())
    return res
  
@app.route("/api/drop/transactions/", methods=["POST"])
def drop_transactions():
    DB.drop_transactions()

    return {}


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=4000, debug=True)
