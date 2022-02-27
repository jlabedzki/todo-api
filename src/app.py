from flask import Flask, request, Response, jsonify
from flask_migrate import Migrate
from flask_bcrypt import Bcrypt
from flask_login import LoginManager, login_user, current_user, logout_user
from db.models import *

app = Flask(__name__)
bcrypt = Bcrypt(app)


# Configure database
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://johnny:johnny@localhost:5432/todo-api'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
migrate = Migrate(app, db)

# Initilialize login manager
login = LoginManager(app)
login.init_app(app)


@login.user_loader
def load_user(id):
    return User.query.get(int(id))


@app.route('/register', methods=['POST'])
def register():
    username = request.json['username']
    password = request.json['password']

    user_exists = db.session.query(db.exists().where(
        User.username == username)).scalar()

    if user_exists:
        return Response(status=409)
    else:
        # hash password before storing in db
        hashed_password = bcrypt.generate_password_hash(password)
        user = User(username=username, password=hashed_password)
        db.session.add(user)
        db.session.commit()
        return Response(status=201)


@app.route('/login', methods=['POST'])
def login():
    username = request.json['username']
    password = request.json['password']

    user = User.query.filter_by(username=username).first()

    if user:
        # Compare the password input to the hashed password in the db
        if bcrypt.check_password_hash(user.password, password):
            login_user(user)
            return jsonify({'user_id': user.id}), Response(status=200)
        else:
            return Response(status=401)
    else:
        return Response(status=404)


@app.route('/logout', methods=['GET'])
def logout():

    logout_user()
    return Response(status=200)


if __name__ == "__main__":
    app.run(debug=True)
