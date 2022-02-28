from flask import Flask, Blueprint, Response, request
from flask_marshmallow import Marshmallow
from db.models import *

app = Flask(__name__)
todos = Blueprint('todos', __name__)

ma = Marshmallow(app)


class TodoSchema(ma.Schema):
    class Meta:
        fields = ('id', 'user_id', 'title', 'date', 'priority', 'completed')


todo_schema = TodoSchema()
todos_schema = TodoSchema(many=True)


@todos.route('/todos/<int:user_id>', methods=['GET', 'POST'])
def todos_for_user(user_id):
    if request.method == 'GET':
        todos = Todo.query.filter_by(user_id=user_id)
        return todos_schema.jsonify(todos), 200

    if request.method == 'POST':
        request.get_json(force=True)

        todo = Todo(
            user_id=user_id,
            title=request.json['title'],
            date=request.json['date']
        )

        db.session.add(todo)
        db.session.commit()
        return todo_schema.jsonify(todo), 201


@todos.route('/todo/<int:todo_id>', methods=['PUT', 'DELETE'])
def update_todo(todo_id):
    if request.method == 'PUT':
        request.get_json(force=True)

        todo = Todo.query.filter_by(id=todo_id).scalar()
        todo.title = request.json['title']
        todo.date = request.json['date']
        todo.priority = request.json['priority']
        todo.completed = request.json['completed']

        db.session.commit()

        return todo_schema.jsonify(todo), 200

    if request.method == 'DELETE':
        todo = Todo.query.filter_by(id=todo_id).scalar()

        db.session.delete(todo)
        db.session.commit()
        return Response(status=200)
