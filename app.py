import json
import os
import subprocess

from flask import Flask, request, jsonify, make_response

from JobHandler import JobHandler
from UserDAO import UserDAO
from ReportDAO import ReportDAO

app = Flask(__name__)

reportDAO = ReportDAO()
userDao = UserDAO()
jobHandler = JobHandler()


# main endpoint, not meant to be used
@app.route("/")
def main():
    return "Route Request to Student Similarity Report Generator"


# login endpoint for existing users
@app.route("/login", methods=['GET', 'OPTIONS'])
def login():
    if request.method == "OPTIONS":  # CORS preflight
        return _build_cors_prelight_response()

    # get the header of the request
    header = request.headers
    # extract the coursecode and password from the header
    coursecode = header.get('coursecode', '')
    passwordIn = header.get('password', '')
    # check if user exists
    exists = userDao.userExists(coursecode)
    if not exists:
        # send response that the user doesnt exist
        return _corsify_actual_response(make_response('{"error": "Course code not found, please sign up"}', 404))

    # check if the password matches
    access = userDao.signIn(coursecode, passwordIn)
    if access == 1:
        # send response that the password is correct
        return _corsify_actual_response(
            make_response('{"status": "Course code found, password correct, access granted!"}', 200))
    # send response that the password was incorrect
    return _corsify_actual_response(make_response('{"error": "Incorrect password, please try again!"', 401))


# sign up endpoint for new users
@app.route("/signup", methods=['POST', 'OPTIONS'])
def signup():
    if request.method == "OPTIONS":  # CORS preflight
        return _build_cors_prelight_response()
    # get data from the body of the request
    data = request.get_json()
    username_in = data.get('coursecode', '')
    password_in = data.get('password', '')
    moss_id = data.get('mossid', '')

    # check if user exists
    exists = userDao.userExists(username_in)
    if exists:
        # if it does respond with an error
        return _corsify_actual_response(make_response(
            '{"error": "That course code already exists, please login or choose a different course code."}', 401))

    # add user
    print(username_in, password_in, moss_id)
    userDao.addUser(username_in, password_in, moss_id)
    # respond that the user was successfully added
    return _corsify_actual_response(make_response('{"status": "User successfully added, signing in now"}', 200))


# endpoint for submitting a job, receives files and submits job to moss
@app.route("/newjob", methods=['POST', 'OPTIONS'])
def receiveFile():
    if request.method == "OPTIONS":  # CORS preflight
        return _build_cors_prelight_response()

    files_found = False
    # uses multi form request, get json from body
    print(request.form.get('data'))
    data = json.loads(request.form.get('data'))
    # get request headers
    print(data)
    header = request.headers

    # get password and coursecode from headers
    password = header.get('password', '')
    coursecode = header.get('coursecode', '')
    # get job name and moss flags from the json/body
    jobname = data.get('jobname', '')
    flag = data.get('flag', '')

    # check if the user exists
    exists = userDao.userExists(coursecode)
    if not exists:
        # send error response if the user does not exist
        return _corsify_actual_response(make_response('{"error": "Course code not found"}', 404))

    # check password
    access = userDao.signIn(coursecode, password)
    if access == 1:
        # checking if user file directory exists
        path = os.path.join("job_src", coursecode, jobname)
        # make the directory if it does not exist
        if not os.path.exists(path):
            print('Making directory: ' + path)
            os.makedirs(path)

        # save files to path
        for archive in request.files.getlist('file[]'):
            if archive.filename != '':
                files_found = True
                if not os.path.exists(os.path.join(path, archive.filename)):
                    archive.save(os.path.join(path, archive.filename))

        # check that files were received
        if not files_found:
            # respond with error if none were received
            return _corsify_actual_response(
                make_response('{"error": "No files found, please upload source code files."}', 404))

        # TODO: Archive

        # make an array of file paths
        files = [os.path.join(path, x) for x in os.listdir(path)]
        print(" ".join(files))

        # instruct reportDAO to make a new report object with status in progress
        reportDAO.addReport(jobname, coursecode)
        # instruct the job handler to start the job
        jobHandler.createJob.delay(files, jobname, coursecode, flag)

        # respond that the job was successfully started
        return _corsify_actual_response(
            make_response('{"status": "Job successfully created and started, please wait for the job to complete."}',
                          200))
    # respond that the password was not correct
    return _corsify_actual_response(make_response('{"error": "Incorrect password"}', 401))


# endpoint for getting all the jobs for a particular user
@app.route("/getalljobs", methods=['GET', 'OPTIONS'])
def getalljobs():
    if request.method == "OPTIONS":  # CORS preflight
        return _build_cors_prelight_response()

    # get the headers from the request
    header = request.headers
    # get the coursecode and password from the headers
    coursecode = header.get('coursecode', '')
    password = header.get('password', '')
    # check if user exists
    exists = userDao.userExists(coursecode)
    if not exists:
        # send error response if the user does not exist
        return _corsify_actual_response(make_response('{"error": "Course code not found"}', 404))

    # check the password
    access = userDao.signIn(coursecode, password)
    if access == 1:
        # send response with all the job information
        return _corsify_actual_response(make_response(reportDAO.getAllJobs(coursecode), 200))
    # send error response that the password was incorrect
    return _corsify_actual_response(make_response('{"error": "Incorrect password"}', 401))


# endpoint for getting a report
@app.route("/getreport", methods=['GET', 'OPTIONS'])
def getreport():
    if request.method == "OPTIONS":  # CORS preflight
        return _build_cors_prelight_response()

    # get headers from request
    header = request.headers
    # fet coursecode password and job name from the headers
    coursecode = header.get('coursecode', '')
    password = header.get('password', '')
    jobname = header.get('jobname', '')

    # check if user exists
    exists = userDao.userExists(coursecode)
    if not exists:
        # send error response if the user does not
        return _corsify_actual_response(make_response('{"error": "Course code not found"}', 404))

    # get password from object
    access = userDao.signIn(coursecode, password)
    if access == 1:
        # TODO check if the report exists / the job has completed
        if True:
            # get the report from the DAO
            reporturl = reportDAO.getReport(jobname, coursecode)
            # send response with the report
            return _corsify_actual_response(make_response('{"rawurl": "' + reporturl + '"}', 200))
        else:
            return _corsify_actual_response(make_response('{"error": "No report found"}', 404))
    # send error response that the password is incomplete
    return _corsify_actual_response(make_response('{"error": "Incorrect password"}', 401))


# endpoint for updating a report from celery process when the job is complete
@app.route("/updatereport", methods=['POST'])
def updatereport():
    # get data from request body
    data = request.get_json()
    # check if the request is coming from celery
    if data.get('id', '') != "BackendSSRG1":
        return 'Invalid ID'

    # get the new report information from the data
    reportName = data.get('reportName', '')
    rawurl = data.get('rawurl', '')
    coursecode = data.get('coursecode', '')
    status = data.get('status', '')
    # update the report
    reportDAO.updateReport(reportName, coursecode, status, rawurl)
    return 'Updated'


# helper function for building a cors preflight response
def _build_cors_prelight_response():
    response = make_response()
    response.headers.add("Access-Control-Allow-Origin", "*")
    response.headers.add('Access-Control-Allow-Headers', "*")
    response.headers.add('Access-Control-Allow-Methods', "*")
    return response

# helper method for adding cors headers to a response
def _corsify_actual_response(response):
    response.headers.add("Access-Control-Allow-Origin", "*")
    return response


# main code executed when the program is run
if __name__ == "__main__":
    # get user
    user = subprocess.check_output("whoami", shell=True).decode("utf-8")
    # set the port and IP based on whether the user is the EC2 instance or not
    print("Running on:", user)
    if (user.strip() == "ubuntu"):
        app.run(debug=True, host="172.31.24.225", port=8080)
    else:
        app.run(debug=True, host="0.0.0.0", port=8000)
