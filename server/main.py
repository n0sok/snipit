import random
import json
import os
import flask
from flask import abort
from flask import render_template
from flask import jsonify
from flask import request
from flask import Flask

app = Flask(__name__)

DB = 'db.txt'

# Web application
@app.route('/')
def index():
    return render_template('index.html')


@app.route('/<path:id>')
def shot(id):
    name = image_by_id(id)
    if not name:
        abort(404)
    return flask.send_from_directory('uploaded', name)


@app.route('/images/<path:name>')
def images(name):
    return flask.send_from_directory('templates/images', name)


def image_by_id(id):
    """Find filename from id."""
    with open(DB) as f:
        for line in f:
            line = line.rstrip()
            row = line.split(',')
            if row[0] == id:
                return row[1]
    return None


# API
# Test
@app.route('/v1/test', methods=['POST'])
def test():
    number = random.randrange(99)
    with open('db.txt', 'a') as f:
        f.write(f'\n{number}')
    d = {'hello': number}
    return jsonify(d)


@app.route('/v1/upload', methods=['POST'])
def upload():
    file = request.files['file']
    filename = file.filename
    file.save(f'{os.getcwd()}/uploaded/{filename}')
    d = {'file': filename}
    # TODO: Save file in "uploaded" directory
    # >TODO: Get random number: 34
    # TODO: Convert current time to timestamp
    # >TODO: Add line to db.txt: open(filename, 'a')
    return jsonify(d)


if __name__ == '__main__':
    app.run(debug=True)
