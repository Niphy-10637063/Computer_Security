
from src.constants.http_status_codes import HTTP_200_OK, HTTP_201_CREATED,HTTP_404_NOT_FOUND, HTTP_409_CONFLICT
from flask import Blueprint, request, jsonify
from flask_jwt_extended import get_jwt_identity, jwt_required
from src.database import User,UserMessage,Message,db
import rsa
user = Blueprint("user", __name__, url_prefix="/api/v1/user")

@user.get('/get/all')
@jwt_required()
def getAllUser():
    currentUserId=get_jwt_identity()
    users = User.query.filter(User.id!=currentUserId).all()
    user_list = []
    for user in users:
        # if user.id != currentUserId:
        user_data = {
            'id': user.id,
            'username': user.username,
        }
        user_list.append(user_data)
    return jsonify({'message': "user list",'data':user_list,"success":True}), HTTP_200_OK

@user.get('/get/publicKey/<int:id>')
@jwt_required()
def getPublicKey(id):
    user = User.query.filter_by(id=id).first()
    if user is None:
        return jsonify({'message': 'User not found',"success":False}), HTTP_404_NOT_FOUND
    user_data = {
        'id': user.id,
        'publicKey': user.publicKey.decode(),
    }

    return jsonify({'message': "user Info",'data':user_data,"success":True}), HTTP_200_OK

@user.post('/sendMessage')
@jwt_required()
def sendMessage():
    message = request.json['message']
    receiverId=request.json['receiverId']
    user = User.query.filter_by(id=receiverId).first()
    publicKey=rsa.PublicKey.load_pkcs1(user.publicKey)
    encryptedMessage=rsa.encrypt(message.encode(),publicKey)
    senderId=get_jwt_identity()

    userMessage = UserMessage(encryptedMessage=encryptedMessage, senderId=senderId,receiverId=receiverId)
    db.session.add(userMessage)
    db.session.commit()

    return jsonify({
        'message': "Message sent successfully",
        'data': {
        },
        "success":True

    }), HTTP_201_CREATED

@user.get('/get/messages')
@jwt_required()
def getMessages():
    userId=get_jwt_identity()
    user = User.query.filter_by(id=userId).first()
    userMessages = UserMessage.query.filter(UserMessage.receiverId==userId).all()
    message_list = []
    for message in userMessages:
        sender = User.query.filter_by(id=message.senderId).first()
        privateKey=rsa.PrivateKey.load_pkcs1(user.privateKey)
        _data = {
            'message':rsa.decrypt(message.encryptedMessage,privateKey).decode(),
            'sender':sender.username,
            'date':message.created_at
        }
        message_list.append(_data)

    return jsonify({
        'message': "list of messages",
        'data': message_list,
        "success":True

    }), HTTP_200_OK

@user.post('/send')
@jwt_required()
def send():
    encryptedMessage = request.json['message']
    senderId=get_jwt_identity()
    userMessage = Message(encryptedMessage=encryptedMessage, senderId=senderId)
    db.session.add(userMessage)
    db.session.commit()

    return jsonify({
        'message': "Message sent successfully",
        'data': {
        },
        "success":True

    }), HTTP_201_CREATED

@user.get('/get')
@jwt_required()
def getMessage():
    userMessages = Message.query.all()
    message_list = []
    for _message in userMessages:
        sender = User.query.filter_by(id=_message.senderId).first()
        _data = {
            'message':_message.encryptedMessage,
            'sender':sender.username,
            'date':_message.created_at
        }
        message_list.append(_data)

    return jsonify({
        'message': "list of messages",
        'data': message_list,
        "success":True

    }), HTTP_200_OK
