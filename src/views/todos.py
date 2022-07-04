from flask import Flask, Blueprint, Response, request
from flask_jwt_extended import jwt_required
from flask_jwt_extended.utils import get_jwt_identity
from flask_marshmallow import Marshmallow
from src.db.models import *

app = Flask(__name__)
todos = Blueprint("todos", __name__)

ma = Marshmallow(app)


class TodoSchema(ma.Schema):
    class Meta:
        fields = ("id", "user_id", "title", "date", "priority", "completed")


todo_schema = TodoSchema()
todos_schema = TodoSchema(many=True)


@todos.route("/todos/<int:user_id>", methods=["GET", "POST"])
@jwt_required()
def todos_for_user(user_id):

    current_user = get_jwt_identity()

    user = User.query.filter_by(id=user_id).first()

    if user.username != current_user:
        return Response(status=403)

    if request.method == "GET":
        todos = Todo.query.filter_by(user_id=user_id)
        return todos_schema.jsonify(todos), 200

    if request.method == "POST":
        request.get_json(force=True)

        todo = Todo(
            user_id=user_id,
            title=request.json["title"],
            date=request.json["date"],
        )

        db.session.add(todo)
        db.session.commit()
        return todo_schema.jsonify(todo), 201


@todos.route("/todo/<int:todo_id>", methods=["PUT", "DELETE"])
@jwt_required()
def update_todo(todo_id):
    if request.method == "PUT":
        request.get_json(force=True)

        todo = Todo.query.filter_by(id=todo_id).scalar()

        if not todo:
            return Response(status=404)

        todo.title = request.json["title"]
        todo.date = request.json["date"]
        todo.priority = request.json["priority"]
        todo.completed = request.json["completed"]

        db.session.commit()

        return todo_schema.jsonify(todo), 200

    if request.method == "DELETE":
        todo = Todo.query.filter_by(id=todo_id).scalar()

        if not todo:
            return Response(status=404)

        db.session.delete(todo)
        db.session.commit()
        return Response(status=200)
