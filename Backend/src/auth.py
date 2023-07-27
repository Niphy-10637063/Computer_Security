
from src.constants.http_status_codes import HTTP_200_OK, HTTP_201_CREATED, HTTP_400_BAD_REQUEST, HTTP_401_UNAUTHORIZED, HTTP_409_CONFLICT
from flask import Blueprint, app, request, jsonify
from werkzeug.security import check_password_hash, generate_password_hash
from flask_jwt_extended import jwt_required, create_access_token, create_refresh_token, get_jwt_identity
import validators
import re
from src.database import User, db
import rsa

auth = Blueprint("auth", __name__, url_prefix="/api/v1/auth")


@auth.post('/register')
def register():
    username = request.json['username']
    email = request.json['email']
    password = request.json['password']
    passwordPattern="(?=.*[A-Za-z])(?=.*\d)(?=.*[!@#$%^&*])[A-Za-z\d!@#$%^&*]{8,}$"
    if not re.match(passwordPattern, password):
        return jsonify({'success':False,'message':'Password should meet the criteria specified','criteria':['Password should contain at least one letter (uppercase or lowercase).',
                                                                                          'Password should contain at least one digit.','Password should contain at least one special character.',
                                                                                          'Password must have a minimum length of 8 characters.']})

    if len(username) < 3:
        return jsonify({'success':False,'message': "Username is too short"}), HTTP_400_BAD_REQUEST

    if  username.isdigit() or  " " in username:
        return jsonify({'success':False,'message': "Username should be alphanumeric, also no spaces"}), HTTP_400_BAD_REQUEST
    
    if len(password) < 8:
        return jsonify({'success':False,'message': "Password is too short"}), HTTP_400_BAD_REQUEST

    if not validators.email(email):
        return jsonify({'success':False,'message': "Email is not valid"}), HTTP_400_BAD_REQUEST

    if User.query.filter_by(email=email).first() is not None:
        return jsonify({'success':False,'message': "Email is taken"}), HTTP_409_CONFLICT

    if User.query.filter_by(username=username).first() is not None:
        return jsonify({'success':False,'message': "username is taken"}), HTTP_409_CONFLICT

    pwd_hash = generate_password_hash(password)
    public_key, private_key = rsa.newkeys(1024)
    publicKey=public_key.save_pkcs1('PEM')
    privateKey=private_key.save_pkcs1('PEM')
    user = User(username=username, password=pwd_hash, email=email,publicKey=publicKey,privateKey=privateKey)
    db.session.add(user)
    db.session.commit()

    return jsonify({
        'message': "User created",
        'data': {
            'username': username, "email": email
        },
        'success':True,

    }), HTTP_201_CREATED

@auth.post('/login')
def login():
    username = request.json.get('username', '')
    password = request.json.get('password', '')

    user = User.query.filter_by(email=username).first()
    if user is None:
        user = User.query.filter_by(username=username).first()

    if user:
        is_pass_correct = check_password_hash(user.password, password)

        if is_pass_correct:
            refresh = create_refresh_token(identity=user.id)
            access = create_access_token(identity=user.id)

            return jsonify({
                'data': {
                    'refresh': refresh,
                    'access': access,
                    'username': user.username,
                    'email': user.email,
                    'userId':user.id,
                },
                'success':True

            }), HTTP_200_OK

    return jsonify({'message': 'Invalid Username/Password'}), HTTP_401_UNAUTHORIZED

@auth.get('/token/refresh')
@jwt_required(refresh=True)
def refresh_users_token():
    identity = get_jwt_identity()
    access = create_access_token(identity=identity)

    return jsonify({
        'access': access
    }), HTTP_200_OK


