from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
db=SQLAlchemy()

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    privateKey=db.Column(db.String(), unique=True, nullable=False)
    publicKey=db.Column(db.String(), unique=True, nullable=False)
    password = db.Column(db.Text(), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.now())
    updated_at = db.Column(db.DateTime, onupdate=datetime.now())


    def __repr__(self) -> str:
        return 'User>>> {self.username}'

class UserMessage(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    encryptedMessage = db.Column(db.String(), unique=True, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.now())
    updated_at = db.Column(db.DateTime, onupdate=datetime.now())
    senderId = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    receiverId = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    # Establish the relationship between the Message and User models
    sender = db.relationship('User', foreign_keys=[senderId], backref='sent_messages')
    receiver = db.relationship('User', foreign_keys=[receiverId], backref='received_messages')
    def __repr__(self) -> str:
        return 'UserMessage>>> {self.id}'
    
class Message(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    encryptedMessage = db.Column(db.String(), unique=True, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.now())
    updated_at = db.Column(db.DateTime, onupdate=datetime.now())
    senderId = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    sender = db.relationship('User', foreign_keys=[senderId], backref='messages')
    def __repr__(self) -> str:
        return 'Message>>> {self.id}'

