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
    #print(username, password)
    if username == "test" and password == "123":
        access = "granted!"
    return access


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=80)
