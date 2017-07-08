from flask import jsonify, request

from extensions import session
from models import Person, Order


def orders():
    return jsonify({'message': 'nothing here'})