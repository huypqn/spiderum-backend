from flask import jsonify
from dataclasses import dataclass
from app import db
from werkzeug.security import generate_password_hash, check_password_hash

user_topic = db.Table(
    'user_topic',
    db.Column('user_id', db.Integer, db.ForeignKey('user.id')),
    db.Column('topic_id', db.Integer, db.ForeignKey('topic.id')) 
)
#------------------------------------------
@dataclass
class User(db.Model):

    id: int
    email: str
    password_hash: str
    name: str
    identity_number: str
    phone_number: str
    address: str
    avatar: str
    wallpaper: str
    sex: str

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(64), index=True, unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)
    name = db.Column(db.String(64), default=str(email).split('@')[0])
    identity_number = db.Column(db.String(32), index=True)
    phone_number = db.Column(db.String(32))
    address = db.Column(db.String(128))
    avatar = db.Column(db.String(256))
    wallpaper = db.Column(db.String(256))
    sex = db.Column(db.String(10))
    posts = db.relationship('Post', backref='author', lazy='dynamic')
    topics = db.relationship('Topic', secondary=user_topic, backref='authors', lazy='dynamic')

    def check_password(self, pw) -> object:
        return check_password_hash(self.password_hash, pw)

    def set_password(self, pw) -> None:
        self.password_hash = generate_password_hash(pw)

    def __repr__(self) -> str:
        return f"<User: {self.name}>"
#------------------------------------------
@dataclass
class Topic(db.Model):

    id: int
    name: str

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), index=True, unique=True, nullable=False)
    posts = db.relationship('Post', backref='topic', lazy='dynamic')

    def __repr__(self) -> str:
        return f"<Topic: {self.name}>"

#------------------------------------------
@dataclass
class Post(db.Model):

    id: int
    title: str
    desc: str
    upvote: int
    comment: int
    view: int
    publish: str
    time_to_read: str
    url: str

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(256), index=True, nullable=False)
    desc = db.Column(db.String(512))
    upvote = db.Column(db.Integer)
    comment = db.Column(db.Integer)
    view = db.Column(db.Integer)
    publish = db.Column(db.String(32))
    time_to_read = db.Column(db.String(32))
    url = db.Column(db.String(256), default='/post')
    thumbnail = db.Column(db.String(256))
    author_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    topic_id = db.Column(db.Integer, db.ForeignKey('topic.id'))

    def __repr__(self) -> str:
        return f"<Post: {self.title}>"

    @staticmethod
    def json_encoder(data, pagination) -> object:
        json_data = []
        for author, email, topic, avatar, post in data:
            encoded = {
                "id": post.id,
                "title": post.title,
                "desc": post.desc,
                "author": author,
                "email": email,
                "username": email.split('@')[0],
                "topic": topic,
                "publish": post.publish,
                "time_to_read": post.time_to_read,
                "upvote": post.upvote,
                "comment": post.comment,
                "view": post.view,
                "url": post.url,
                "thumbnail": post.thumbnail,
                "avatar": avatar
            }
            json_data.append(encoded)
        
        return {
            "data": json_data,
            "pagination": pagination
        }