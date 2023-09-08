"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
from flask_jwt_extended import create_access_token, get_jwt_identity, jwt_required
from flask import Flask, request, jsonify, url_for, Blueprint, current_app
from api.models import db,User,Planets,People,Favorites
from api.utils import generate_sitemap, APIException
import json


api = Blueprint('api', __name__)


@api.route('/hello', methods=['POST', 'GET'])
def handle_hello():

    response_body = {
        "message": "Hello! I'm a message that came from the backend, check the network tab on the google inspector and you will see the GET request"
    }

    return jsonify(response_body), 200


@api.route('/signup', methods=['POST'])
def signup_user():
    body = json.loads(request.data)
    pw_hash = current_app.bcrypt.generate_password_hash(body["password"]).decode('utf-8')

    new_user = User(
        name = body["name"],
        lastname = body["lastname"],
        email = body["email"],
        password = pw_hash

    )
    db.session.add(new_user)
    db.session.commit()
    


    response_body = {
        "message": "usuario creado correctamente"
    }

    return jsonify(response_body), 200


@api.route('/login', methods=['POST'])
def login_user():
    body = json.loads(request.data)
    user = User.query.filter_by(email=body["email"]).first()

    if user is None: 
        return jsonify({"msg": "not found"}), 404
    
    pw_hash = current_app.bcrypt.check_password_hash(user.password,body["password"])
    if not pw_hash:
        return jsonify({"msg": "email or password are incorrect"}), 401 
    access_token = create_access_token(identity=body["email"])
    return jsonify(access_token=access_token), 200

    