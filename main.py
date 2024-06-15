from flask import Flask, request, jsonify, send_file
import json
import os
from datetime import datetime

app = Flask(__name__)

comments = []

# Load comments from comments.json initially
if os.path.exists('comments.json'):
    with open('comments.json', 'r') as f:
        comments = json.load(f)

# Endpoint to show comments
@app.route('/show', methods=['GET'])
def show_comments():
    return jsonify(comments)

# Endpoint to receive and store new comment
@app.route('/send', methods=['POST'])
def send_comment():
    data = request.get_json()
    name = data.get('name')
    comment = data.get('comment')
    if not name or not comment:
        return 'Your Name/Comment is undefined :(', 400

    date = datetime.now().strftime("%m-%d-%Y")
    new_comment = {
        "name": name,
        "comment": comment,
        "date": date
    }
    comments.append(new_comment)

    with open('comments.json', 'w') as f:
        json.dump(comments, f, indent=2)

    return 'Success Send!'

# Endpoint to serve different scripts based on key type
@app.route('/script', methods=['GET'])
def get_script():
    date = datetime.now().strftime("%m-%d-%Y")
    key = request.args.get('key')
    with open('k.json', 'r') as f:
        keys = json.load(f)

    if key in keys:
        script_type = keys[key]['type']
        if keys['exp'] == date:
            return "Your Key is Expired.", 400
        if script_type == 'Free':
            return send_file('./src/free-script.lua')
        elif script_type == 'VIP':
            return send_file('./src/vip_script-TSBNS.lua')
        else:
            return 'Unknown script type', 400
    else:
        return 'Key is Invalid!', 400

# Start the server
if __name__ == '__main__':
    app.run(port=8080)