from flask import Flask, redirect, jsonify
from flask_login import LoginManager, login_user, current_user, logout_user
from db.models import *

app = Flask(__name__)

# Configure database
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://johnny:johnny@localhost:5432/todo-api'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Initilialize login manager
login = LoginManager(app)
login.init_app(app)


@app.route('/', methods=['GET'])
def index():
    return jsonify({"hello": "world"})


if __name__ == "__main__":
    app.run(debug=True)
