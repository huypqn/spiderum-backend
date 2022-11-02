from flask import jsonify
from app import app
from app.models import db, User, Topic, Post

@app.route('/v1/api/?page=<int:index>')
def get_posts(index):
    return 

@app.route('/v1/api/topic')
def get_topic():
    topics = db.session.query(User).all()
    return jsonify(topics)
