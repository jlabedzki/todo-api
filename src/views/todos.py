from flask import Flask, Blueprint, Response, jsonify, request
from db.models import *

app = Flask(__name__)
todos = Blueprint('todos', __name__)

# @app.route('/todos/:user', methods=['GET', 'POST'])
# @app.route('/todo/:id', methods=['POST'])
