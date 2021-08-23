import json

from flask import Flask, request, jsonify

app = Flask(__name__)


@app.route("/")
def main():
    return "Route Request to Student Similarity Report Generator"


@app.route("/login", methods=['GET'])
def login():
    data = request.get_json()
    usernameIn = data.get('username', '')
    passwordIn = data.get('password', '')
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
    data = request.get_json()
    username_in = data.get('username', '')
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

    # other job info like MOSS flags included here

    # check password
    for archive in request.files.getlist('file'):
        if archive.filename != '':
            files_found = True
            archive.save("job_src/" + username + "/" + jobname + "/" + archive.filename)

    if files_found:
        return "success", 200
    return "no files found", 404


if __name__ == "__main__":
    app.run(debug=True, host="172.31.24.225", port=8080)
    # app.run(debug=True, host="0.0.0.0", port=8000)
