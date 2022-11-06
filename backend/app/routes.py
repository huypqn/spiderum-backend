from flask import request, jsonify
from flask_restful import Resource
from sqlalchemy import func
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
        category = request.args.get("cat_id", type=int)
        total = db.session.query(func.count(Post.id)).scalar()
        pagination = {
            "page": page,
            "limit": limit,
            "total": total
        }

        query = db.session.query(User.name, User.email, Topic.name, User.avatar, Post)\
                            .join(User)\
                            .join(Topic)
        match type:
            case "trending":
                trending = query.order_by(Post.view.desc())
                if category:
                    trending = trending.filter(Topic.id == category)
                
                trending = trending.limit(4).all()
                return Post.json_encoder(trending, {})

            case "popular":
                popular = query.order_by(Post.upvote.desc())
                if category:
                    popular = popular.filter(Topic.id == category)
                
                popular = popular.limit(4).all()
                return Post.json_encoder(popular, {})

        if page:
            posts = query.paginate(page=page, per_page=limit, error_out=False).items
            return Post.json_encoder(posts, pagination)

        data = query.all()
        return Post.json_encoder(data, pagination)

    def post(self):
        return