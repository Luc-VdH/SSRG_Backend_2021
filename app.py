import json
import os

from celery import Celery
from flask import Flask, request, jsonify

from JobHandler import JobHandler

app = Flask(__name__)

jobHandler = JobHandler()


@app.route("/")
def main():
    return "Route Request to Student Similarity Report Generator"


@app.route("/login", methods=['GET'])
def login():
    # data = request.get_json()
    # usernameIn = data.get('username', '')
    # passwordIn = data.get('password', '')

    header = request.headers
    usernameIn = header.get('coursecode', '')
    passwordIn = header.get('password', '')
    # check if user exists
    exists = True
    if not exists:
        return "user not found", 404

    # get password from object
    passwordS = "123"
    print(usernameIn, passwordIn)
    if passwordIn == passwordS:
        return "Granted", 200
    return "Denied!", 401


@app.route("/signup", methods=['GET'])
def signup():
    data = request.headers
    username_in = data.get('coursecode', '')
    password_in = data.get('password', '')
    moss_id = data.get('mossid', '')

    # check if user exists
    exists = False
    if exists:
        return "user already exists", 401

    # add user
    print(username_in, password_in, moss_id)
    return "user added", 200


@app.route("/newjob", methods=['POST'])
# @app.route("/uploadfile/<course_code>/<job_name>", methods=['POST'])
def receiveFile():
    files_found = False

    print(request.form.get('data'))
    data = json.loads(request.form.get('data'))
    print(data)

    password = data.get('password', '')
    username = data.get('username', '')
    jobname = data.get('jobname', '')
    flag = data.get('flag', '')

    # other job info like MOSS flags included here

    # checking if user file directory exists
    path = os.path.join("job_src", username, jobname)
    if not os.path.exists(path):
        os.makedirs(path)
    else:
        print(path + ' is valid')

    # TODO check password

    # save files to path
    for archive in request.files.getlist('file[]'):
        if archive.filename != '':
            files_found = True
            if not os.path.exists(os.path.join(path, archive.filename)):
                archive.save(os.path.join(path, archive.filename))

    if not files_found:
        return "no files found", 404

    files = [os.path.join(path, x) for x in os.listdir(path)]
    print(" ".join(files))

    jobHandler.createJob.delay(files, jobname, username, flag)

    return "success", 200


if __name__ == "__main__":
    app.run(debug=True, host="172.31.24.225", port=8080)
    # app.run(debug=True, host="0.0.0.0", port=8000)
