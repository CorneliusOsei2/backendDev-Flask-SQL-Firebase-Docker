import json

from flask import Flask
from flask import jsonify
from flask import request

app = Flask(__name__)

posts = {
    0: {
        "id": 0,
        "upvotes": 1,
      "title": "My cat is the cutest!",
      "link": "https://i.imgur.com/jseZqNK.jpg",
      "username": "alicia98",
      "comments": {1:
                    {
                    "id": 0,
                    "upvotes": 8,
                    "text": "Wow, my first Reddit gold!",
                    "username": "alicia98",
                    }
      }
    },

    1: {"id": 1,
      "upvotes": 3,
      "title": "Cat loaf",
      "link": "https://i.imgur.com/TJ46wX4.jpg",
      "username": "alicia98",
      "comments": {1 :
                    {
                    "id": 1,
                    "upvotes": 9,
                    "text": "Where is the cat!",
                    "username": "alicwewia98",
                    }
      }
    }
}


posts_counter = 2
comments_counter = 2

@app.route("/")
def hello_world():
    return "Hello world!"

@app.route("/api/posts/")
def get_posts():
    '''
        Gets all posts
    '''
    all_posts = []

    for key, post in posts.items():
        temp = {
            "id": post["id"],
            "upvotes": post["upvotes"],
            "title" : post["title"],
            "link" : post["link"],
            "username" : post["username"]
        }

        all_posts.append(temp)

    res = {"posts": all_posts}
    return json.dumps(res), 200

@app.route("/api/posts/", methods=["POST"])
def create_post():
    '''
        Creates a post
    '''

    global posts_counter

    try:
        req_body = json.loads(request.data)
        post = {
            "id" : posts_counter,
            "upvotes" : 1,
            "title": req_body["title"],
            "link" : req_body["link"],
            "username" : req_body["username"],
            "comments": {}
        }

        temp = post
        post["comments"] = {}
        posts[posts_counter] = post
        posts_counter += 1

        return json.dumps(temp), 201
    except:
        return json.dumps({"error": "Complete all input fields: title, link, username"}), 400


@app.route("/api/posts/<int:post_id>", methods=["GET"])
def get_post(post_id):
    '''
        Gets post with id <post_id>
    '''

    if post_id not in posts:
        return json.dumps({"error" : "No such post exists"}), 404

    post = posts[post_id]
    temp = {
    "id": post["id"],
    "upvotes": post["upvotes"],
    "title" : post["title"],
    "link" : post["link"],
    "username" : post["username"]
    }
    return json.dumps(temp), 200


@app.route("/api/posts/<int:post_id>", methods=["DELETE"])
def delete_post(post_id):
    '''
        Deletes the post with id <post_id>
    '''

    if post_id not in posts:
        return json.dumps({"error" : "No such post exists"}), 404
    
    deleted_post = posts[post_id]

    res = {
    "id": post_id,
    "upvotes": deleted_post["upvotes"],
    "title": deleted_post["title"],
    "link": deleted_post["link"],
    "username": deleted_post["username"]
    }

    del posts[post_id]
    return json.dumps(res), 200
    

@app.route("/api/posts/<int:post_id>/comments/", methods=["GET"])
def get_post_comment(post_id):
    '''
        Gets the comments of a post with id <post_id>
    '''

    if post_id not in posts:
        return json.dumps({"error" : "No such post exists"}), 404

    post = posts[post_id]
    res = {"comments": list(post["comments"].values())}

    return json.dumps(res), 200


@app.route("/api/posts/<int:post_id>/comments", methods=["POST"])
def create_comment(post_id):
    '''
        Create comment for post with id <post_id>
    '''

    global comments_counter
    try:
        req_body = json.loads(request.data)
        new_comment = {
            "id": comments_counter,
            "upvotes": 1,
            "text": req_body["text"],
            "username": req_body["username"]
        }

        posts[post_id]["comments"][comments_counter] = new_comment
        comments_counter += 1

        return json.dumps(new_comment), 201
    except:
        return json.dumps({"error": "Complete all input fields: text, username"}), 400

# Edit a comment of a post.
@app.route("/api/posts/<int:post_id>/comments/<int:comment_id>", methods=["POST"])
def edit_comment(post_id, comment_id):
    '''
        Edits comment with id <comment_id> of post with id <post_id>
    '''

    if post_id not in posts:
        return json.dumps({"error": "No such post exists"}), 404
    
    if comment_id not in posts[post_id]["comments"]:
        return json.dumps({"error": "No such comment exists"}), 404

    try:
        req_body = json.loads(request.data)
        posts[post_id]["comments"][comment_id]["text"] = req_body["text"]
        res = posts[post_id]["comments"][comment_id]

        print(res)
        return json.dumps(res), 200
    except:
        return json.dumps({"error": "Complete input field: text"}), 400


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=2000, debug=True)
