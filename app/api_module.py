from flask import request, jsonify, url_for
from flask_restful import Resource
from sqlalchemy import func
from app import app, api
from app.models import db, User, Topic, Post
from app.services import verify_register_token

@api.resource('/v1/api/user/register')
class UserRegisterResource(Resource):
    def get(self):
        args = request.args
        return

    def post(self):
        payload = request.get_json()
        token = payload.get('token')
        # verify = verify_register_token(token)
        if token == "123":
            verify = {
                "code": 200,
                "message": "accepted"
            }
        else:
            verify = {
                "code": 401,
                "message": "Có lỗi xảy ra. Xin vui lòng thử lại sau!"
            }
        if verify.get('code') == 200:
            username = payload.get('username')
            user = db.session.query(User).filter_by(username=username).first()
            if user:
                return {
                    "code": 409,
                    "message": "Tên đăng nhập đã tồn tại!"
                }
            password = payload.get('password')
            name = payload.get('name') if payload.get('name') else username
            identity = payload.get('identity_number') or None
            phone_number = payload.get('phone_number') or None
            user = User(
                username=username,
                email="test@example.com",
                name=name,
                identity_number=identity,
                phone_number=phone_number,
                avatar="https://www.gravatar.com/avatar/b5810e9b3bc27b71948c4d303e0c80ca?d=wavatar&f=y"
            )
            user.set_password(password)
            db.session.add(user)
            try:
                db.session.commit()
                return {
                    "code": 200,
                    "message": "Đăng ký thành công. Bạn sẽ được chuyển hướng về trang chủ sau 3s!"
                }
            except:
                return {
                    "code": 503,
                    "message": "Có lỗi xảy ra. Xin vui lòng thử lại sau!"
                }
        
        else:
            return verify

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