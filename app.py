import json
import os
import subprocess

from celery import Celery
from flask import Flask, request, jsonify, make_response

from JobHandler import JobHandler
from UserDAO import UserDAO
from ReportDAO import ReportDAO

app = Flask(__name__)

reportDAO = ReportDAO()
userDao = UserDAO()
jobHandler = JobHandler()
jobHandler.setReportDAO(reportDAO)

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


@app.route("/signup", methods=['POST', 'OPTIONS'])
def signup():
    if request.method == "OPTIONS":  # CORS preflight
        return _build_cors_prelight_response()
    data = request.get_json()
    username_in = data.get('coursecode', '')
    password_in = data.get('password', '')
    moss_id = data.get('mossid', '')

    # check if user exists
    exists = userDao.userExists(username_in)
    if exists:
        return _corsify_actual_response(make_response("That course code already exists, please login or choose a different course code.", 401))

    # add user
    print(username_in, password_in, moss_id)
    userDao.addUser(username_in, password_in, moss_id)
    return _corsify_actual_response(make_response("User successfully added, signing in now", 200))


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

    password = data.get('password', '')
    coursecode = data.get('coursecode', '')
    jobname = data.get('jobname', '')
    flag = data.get('flag', '')
    exists = userDao.userExists(coursecode)
    if not exists:
        return _corsify_actual_response(make_response("Course code not found", 404))
    
    access = userDao.signIn(coursecode, password)
    if access == 1:
        # checking if user file directory exists
        path = os.path.join("job_src", coursecode, jobname)
        if not os.path.exists(path):
            print('Making directory: ' + path)
            os.makedirs(path)

        # save files to path
        for archive in request.files.getlist('file[]'):
            if archive.filename != '':
                files_found = True
                if not os.path.exists(os.path.join(path, archive.filename)):
                    archive.save(os.path.join(path, archive.filename))

        if not files_found:
            return _corsify_actual_response(make_response("No files found, please upload source code files.", 404))
        
        #TODO: Archive
        
        files = [os.path.join(path, x) for x in os.listdir(path)]
        print(" ".join(files))
        
        jobHandler.createJob.delay(files, jobname, coursecode, flag)
        
        return _corsify_actual_response(make_response("Job successfully created and started, please wait for the job "
                                                      "to complete.", 200))
    return _corsify_actual_response(make_response("Incorrect password", 401))


@app.route("/getalljobs", methods=['GET', 'OPTIONS'])
def getalljobs():
    if request.method == "OPTIONS":  # CORS preflight
        return _build_cors_prelight_response()

    header = request.headers
    username = header.get('coursecode', '')
    password = header.get('password', '')
    # check if user exists
    exists = userDao.userExists(username)
    if not exists:
        return _corsify_actual_response(make_response("Course code not found", 404))

    # get password from object
    access = userDao.signIn(username, password)
    if access == 1:
        reportDAO.initReports()
        return _corsify_actual_response(make_response(reportDAO.getAllJobs(username), 200))

    return _corsify_actual_response(make_response("Incorrect password", 401))


@app.route("/getreport", methods=['GET', 'OPTIONS'])
def getreport():
    if request.method == "OPTIONS":  # CORS preflight
        return _build_cors_prelight_response()

    header = request.headers
    username = header.get('coursecode', '')
    password = header.get('password', '')
    jobname = header.get('jobname', '')

    # check if user exists
    exists = userDao.userExists(username)
    if not exists:
        return _corsify_actual_response(make_response("Course code not found", 404))

    # get password from object
    access = userDao.signIn(username, password)
    if access == 1:
        # get report
        if True:
            return _corsify_actual_response(make_response("Report", 200))
        else:
            return _corsify_actual_response(make_response("No report found", 404))
    return _corsify_actual_response(make_response("Incorrect password", 401))


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
    user = subprocess.check_output("whoami", shell=True).decode("utf-8") 
    print("Running on:", user)
    if(user.strip() == "ubuntu"):
        app.run(debug=True, host="172.31.24.225", port=8080)
    else:
        app.run(debug=True, host="0.0.0.0", port=8000)
