import json

from flask import Flask, request, jsonify

app = Flask(__name__)


@app.route("/")
def main():
    return "Hello World"


@app.route("/test")
def test():
    access = "denied!"
    data = request.get_json()
    username = data.get('username', '')
    password = data.get('password', '')
    # print(username, password)
    if username == "test" and password == "123":
        access = "granted!"
    return access


@app.route("/signin", methods=['GET'])
def signin():
    access = "denied!"
    data = request.get_json()
    usernameIn = data.get('username', '')
    passwordIn = data.get('password', '')
    file = open("usrs/" + usernameIn + ".txt")
    passwordS = file.readline().strip()
    print(passwordS)
    if passwordIn == passwordS:
        access = "granted!"
    return access


@app.route("/newjob", methods=['POST'])
# @app.route("/uploadfile/<course_code>/<job_name>", methods=['POST'])
def receiveFile():
    success = "no files found"
    course_code = ""
    data = json.load(request.files['data'])
    archive = request.files['file']

    password = data.get('password', '')
    username = data.get('username', '')
    jobname = data.get('jobname', '')
    # other job info like MOSS flags included here

    # check password
    if archive.filename != '':
        success = "upload successful"
        archive.save("job_src/" + username + "/" + jobname + "/" + archive.filename)

    return success


if __name__ == "__main__":
    # app.run(debug=True, host="172.31.24.225", port=8080)
    app.run(debug=True, host="0.0.0.0", port=8080)
