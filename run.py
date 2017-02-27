import os


# imports app from views. This is to "start" the flask app.
from pig.views import app


# Setup of hosting
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)

