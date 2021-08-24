import json
import os

from celery import Celery
from flask import Flask, request, jsonify, make_response

from JobHandler import JobHandler
from UserDAO import UserDAO

app = Flask(__name__)

jobHandler = JobHandler()
userDao = UserDAO()


@app.route("/")
def main():
    return "Route Request to Student Similarity Report Generator"


@app.route("/login", methods=['GET', 'OPTIONS'])
def login():
    # data = request.get_json()
    # usernameIn = data.get('username', '')
    # passwordIn = data.get('password', '')
    if request.method == "OPTIONS":  # CORS preflight
        return _build_cors_prelight_response()

    header = request.headers
    usernameIn = header.get('coursecode', '')
    passwordIn = header.get('password', '')
    # check if user exists
    exists = userDao.userExists(usernameIn)
    if not exists:
        return _corsify_actual_response(make_response("Course code not found, please sign up", 404))

    # get password from object
    access = userDao.signIn(usernameIn, passwordIn)
    if access == 1:
        return _corsify_actual_response(make_response("Course code found, password correct, access granted!", 200))
    return _corsify_actual_response(make_response("Incorrect password, please try again!", 401))


@app.route("/signup", methods=['POST'])
def signup():
    data = request.get_json()
    username_in = data.get('coursecode', '')
    password_in = data.get('password', '')
    moss_id = data.get('mossid', '')

    # check if user exists
    exists = False
    if exists:
        return "That course code already exists, please login or choose a different course code.", 401

    # add user
    print(username_in, password_in, moss_id)
    return "User successfully added, signing in now", 200


@app.route("/newjob", methods=['POST', 'OPTIONS'])
# @app.route("/uploadfile/<course_code>/<job_name>", methods=['POST'])
def receiveFile():
    if request.method == "OPTIONS":  # CORS preflight
        return _build_cors_prelight_response()

    files_found = False

    print(request.form.get('data'))
    data = json.loads(request.form.get('data'))
    print(data)
    header = request.headers

    password = header.get('password', '')
    coursecode = header.get('coursecode', '')
    jobname = data.get('jobname', '')
    flag = data.get('flag', '')

    # other job info like MOSS flags included here

    # checking if user file directory exists
    path = os.path.join("job_src", coursecode, jobname)
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
        return _corsify_actual_response(make_response("No files found, please upload source code files.", 404))

    files = [os.path.join(path, x) for x in os.listdir(path)]
    print(" ".join(files))

    jobHandler.createJob.delay(files, jobname, coursecode, flag)

    return _corsify_actual_response(make_response("Job successfully created and started, please wait for the job to "
                                                  "complete.", 200))


def _build_cors_prelight_response():
    response = make_response()
    response.headers.add("Access-Control-Allow-Origin", "*")
    response.headers.add('Access-Control-Allow-Headers', "*")
    response.headers.add('Access-Control-Allow-Methods', "*")
    return response


def _corsify_actual_response(response):
    response.headers.add("Access-Control-Allow-Origin", "*")
    return response


if __name__ == "__main__":
    app.run(debug=True, host="172.31.24.225", port=8080)
    # app.run(debug=True, host="0.0.0.0", port=8000)
