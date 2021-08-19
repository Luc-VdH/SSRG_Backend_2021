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


@app.route("/uploadfile/", methods=['POST'])
@app.route("/uploadfile/<course_code>/<job_name>", methods=['POST'])
def receiveFile(course_code="none", job_name="None"):
    success = "no files found"

    if course_code != "none":
        for uploaded_file in request.files.getlist('file'):
            if uploaded_file.filename != '':
                uploaded_file.save("job_src/" + course_code + "/" + job_name + "/" + uploaded_file.filename)
                success = "upload successful"
    else:
        success = "no course code found"

    return success


if __name__ == "__main__":
    app.run(debug=True, host="172.31.24.225", port=8080)
    # app.run(debug=True, host="0.0.0.0", port=8080)
