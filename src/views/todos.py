from flask import Flask, Blueprint, Response, request
from flask_marshmallow import Marshmallow
from db.models import *

app = Flask(__name__)
todos = Blueprint('todos', __name__)

ma = Marshmallow(app)


class TodoSchema(ma.Schema):
    class Meta:
        fields = ('id', 'user_id', 'title', 'created_at', 'status_id')


todo_schema = TodoSchema()
todos_schema = TodoSchema(many=True)


@todos.route('/todos/<user_id>', methods=['GET', 'POST'])
def todos_for_user(user_id):
    # request.get_json(force=True)

    if request.method == 'GET':
        todos = Todo.query.filter_by(user_id=user_id)
        return todos_schema.jsonify(todos)

    if request.method == 'POST':
        request.get_json(force=True)

        todo = Todo(
            user_id=user_id,
            title=request.json['title'],
            created_at=request.json['date']
        )

        db.session.add(todo)
        db.session.commit()
        return todo_schema.jsonify(todo)


@todos.route('/todo/<todo_id>', methods=['PUT', 'DELETE'])
def update_todo(todo_id):
    if request.method == 'POST':
        return

    if request.method == 'DELETE':
        todo = Todo.query.filter_by(id=todo_id).scalar()

        if todo:
            db.session.delete(todo)
            db.session.commit()
            return Response(status=200)

        return Response(status=404)
