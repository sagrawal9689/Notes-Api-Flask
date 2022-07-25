import datetime
from functools import wraps
from flask import Blueprint, request, jsonify
from Notes.models import User
from werkzeug.security import generate_password_hash, check_password_hash
from . import db
import jwt

auth= Blueprint('auth',__name__)

@auth.route('/login',methods=['POST'])
def login():
    
    if not 'email' in request.json:
        return jsonify('Please enter your Email.'),400
    
    if not 'password' in request.json:
        return jsonify('Please enter a Password.'),400

    email = request.json['email']
    password = request.json['password']
    
    if not email or not password:
        return jsonify('Please provide email and password!'),400

    user = User.query.filter_by(email=email).first()
    if user:
        if check_password_hash(user.password, password):
            token = jwt.encode({'id' : user.id , 'exp' : datetime.datetime.utcnow() + datetime.timedelta(minutes=30)}, 'secret')

            return jsonify({'token' : token, 'email': user.email , 'name' : user.name})
        else:
            return jsonify('Incorrect password, try again.'),401
    else:
        return jsonify('Email does not exist.'),401
    



@auth.route('/sign-up', methods=['POST'])
def sign_up():
    
    if not 'name' in request.json:
        return jsonify('Please enter a Name.'),400

    if not 'email' in request.json:
        return jsonify('Please enter your Email.'),400
    
    if not 'password' in request.json:
        return jsonify('Please enter a Password.'),400

    name = request.json['name']
    email = request.json['email']
    password = request.json['password']

    user = User.query.filter_by(email=email).first()
    if user:
        return jsonify('Email already exists.'),400
    elif len(email) < 4:
        return jsonify('Email must be greater than 3 characters.'),400
    elif len(name) < 2:
        return jsonify('First name must be greater than 1 character.'),400
    elif len(password) < 7:
        return jsonify('Password must be at least 7 characters.'),400
    else:
        new_user = User(email=email, name=name, password=generate_password_hash(
            password, method='sha256'))
        db.session.add(new_user)
        db.session.commit()

    return jsonify('New user created!'), 201