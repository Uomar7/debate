from . import db
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from . import login_manager
from datetime import datetime


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class User(UserMixin, db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(255), index=True)
    email = db.Column(db.String(255), unique=True, index=True)
    bio = db.Column(db.String(255))
    profile_pic_path = db.Column(db.String())
    password_hash = db.Column(db.String(255))

    # chats = db.relationship('Chat', backref='user', lazy="dynamic")
    debates = db.relationship('Debate', backref='user', lazy="dynamic")

    @property
    def password(self):
        raise AttributeError('You cannot read the password attribute')

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return f'User {self.username}'


class Category(db.Model):
    __tablename__ = "categories"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255))


class Debate(db.Model):
    __tablename__ = 'debates'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255))
    text = db.Column(db.String)
    title = db.Column(db.String)
    username = db.Column(db.String(255), index=True)
    debate_id = db.Column(db.Integer)
    category = db.Column(db.String(255))
    posted = db.Column(db.DateTime, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))

    # chats = db.relationship('Chat', backref='debates', lazy='dynamic')

    def save_debate(self):
        db.session.add(self)
        db.session.commit()

    def get_debates(self):
        debates = Debate.query.all()
        return debates

    def get_debate(self):
        debate = Debate.query.filter_by(debate_id)
        return debate

    def __repr__(self):
        return f'User {self.name}'


class Chat(db.Model):

    __tablename__ = 'chats'

    id = db.Column('id', db.Integer, primary_key=True)
    # debate_id = db.Column(db.Integer, db.ForeignKey('debates.id'))
    # username = db.Column(db.String(255), index=True)
    # chat_id = db.Column(db.Integer)
    # title = db.Column(db.String)
    chat = db.Column(db.String)
    # posted = db.Column(db.DateTime, default=datetime.utcnow)
    # user_id = db.Column(db.Integer, db.ForeignKey("users.id"))

    # def save_chat(self):
    #     db.session.add(self)
    #     db.session.commit()

    # def get_chats(self):
    #     chats = Chat.query.all()
    #     return chats

    # def get_chat(self):
    #     chat = Chat.query.filter_by(chat_id)
    #     return chat
