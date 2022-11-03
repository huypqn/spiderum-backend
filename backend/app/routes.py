from flask import request, jsonify
from flask_restful import Resource
from app import app, api
from app.models import db, User, Topic, Post

@api.resource('/v1/api/user')
class UserResource(Resource):
    def get(self):
        args = request.args
        return

    def post(self):
        return

    def patch(self):
        return
#-------------------------
@api.resource('/v1/api/topic')
class TopicResource(Resource):
    def get(self):
        data = db.session.query(Topic).all()
        return jsonify(data)
#-------------------------
@api.resource('/v1/api/post')
class PostResource(Resource):
    def get(self):
        type = request.args.get("type")
        page = request.args.get("page", type=int)
        limit = request.args.get("limit", app.config['POSTS_PER_PAGE'], type=int)

        query = db.session.query(User.name, Topic.name, Post).join(User).join(Topic)
        match type:
            case "trending":
                trending = query.order_by(Post.view.desc()).limit(4).all()
                return Post.json_encoder(trending)

            case "popular":
                popular = query.order_by(Post.comment.desc()).limit(4).all()
                return Post.json_encoder(popular)

        if page:
            posts = query.paginate(page=page, per_page=limit, error_out=False).items

            return Post.json_encoder(posts)

        data = query.all()
        return Post.json_encoder(data)

    def post(self):
        return