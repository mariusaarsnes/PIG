import os
from flask import Flask

app = Flask(__name__)

@app.route("/")
def hello():
    return "Hello world!"

# Heroku assigns the port number, given en the env variable PORT - we need to use this one
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
