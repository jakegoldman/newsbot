import uuid
from datetime import datetime
from flask import (
    Flask,
    request,
    abort,
    jsonify,
)
import json

app = Flask(__name__)

users = []
chat = [] # Hold messages
messages = dict()
keyword = ""
@app.route("/")
def hello():
    return "hello\n"

@app.route('/login', methods=["POST"])
def login():
    username = request.json.get('username', None)
    if username is None or username in users:
        abort(401)
    else:
        users.append(username)
        print(username)
        return jsonify({
            'status': 'OK',
            'message' : "Successfully Logged in"
        })


@app.route("/send", methods=["POST"])
def send():
    username = request.json.get('username', None)
    message = request.json.get('message', None)

    if username is None or username not in users:
        abort(401)

    if message is None or message == '':
        abort(400)

    id = str(uuid.uuid4())

    messages[id] = {
        'username': username,
        'message': message,
        'timestamp': datetime.now(),
        'id': id,
    }
    chat.append(id)
    # return jsonify(messages)
    return jsonify({"id": id,})


@app.route('/get', defaults={'last_id': None})

@app.route("/get/<last_id>", methods=["GET"])
def get(last_id):
    if chat is None or len(chat) == 0:
        return []

    index = get_next_index(last_id) if last_id else 0
    ids_to_return = chat[index:]
    results = map(lambda x : messages[x], ids_to_return)
    # return jsonify(list(results))
    return jsonify(sorted(results, key=[lambda x: x['timestamp']]))

@app.route("/updates/<last_id>", methods=["GET"])
def updates(last_id):
    index = get_next_index(last_id) if last_id else 0
    result = {
        'new_messages': False
    }

    # if index < len(chat) - 1:
    #  result['new_messages'] = True
    #return jsonify(result)
    if index is None or len(chat) is None:
        result['new_messages'] = False
    elif index < len(chat):
       result['new_messages'] = True
    return jsonify(result)


@app.route("/search/<keyword>", method = ["GET"])
def get(keyword):
    keyword = keyword
    return "You are interested in "+keyword



def get_next_index(last_id):
    try:
        return chat.index(last_id)
    except ValueError as e:
        abort(400)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
