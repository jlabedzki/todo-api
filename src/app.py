import os
from flask import Flask
from flask_login import LoginManager
from flask_migrate import Migrate
from decouple import config
from db.models import *
from views.authentication import authentication
from views.todos import todos

app = Flask(__name__)
# Add secret key
app.config.update(SECRET_KEY=os.urandom(24))

# Configure database
app.config['SQLALCHEMY_DATABASE_URI'] = config('DATABASE_URI')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
migrate = Migrate(app, db)


# Initilialize login manager
login = LoginManager(app)
login.init_app(app)


@login.user_loader
def load_user(id):
    return User.query.get(int(id))


app.register_blueprint(authentication)
app.register_blueprint(todos)


if __name__ == "__main__":
    app.run(debug=True)
