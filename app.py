from argparse import ArgumentParser
from dotenv import load_dotenv

parser = ArgumentParser()
parser.add_argument("--config", type=str, default="./configs/example.env")
args = parser.parse_args()

# IMPORTANT: this need to be run before all other imports
if args.config != 0:
    load_dotenv(args.config)
# only import other class after this

from flask import Flask, request, render_template, redirect, make_response
from flask_cors import CORS


from src.database import USER, Session
from src.api import api
from src.routes import routes

app = Flask(__name__)
CORS(app)

app.register_blueprint(api)
app.register_blueprint(routes)


@app.teardown_appcontext
def shutdown_session(exception=None):
    ''' Enable Flask to automatically remove database sessions at the
    end of the request or when the application shuts down.
    Ref: https://flask.palletsprojects.com/en/2.3.x/patterns/sqlalchemy/
    '''
    Session.remove()

if __name__ == "__main__":
    app.run(debug=True)
