from flask import Flask
app = Flask(__name__)

@app.route("/")
def hello():
    return "Hello World!"

@app.route("/all")
def helloAll():
    return "Hello All!"

if __name__ == "__main__":
    app.run()
