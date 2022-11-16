import jwt
from flask import request, jsonify, make_response
from app import app
from app.models import db, User
from app.email import send_register_email

@app.route('/v1/api/register', methods=['GET', 'POST'])
def register():
    email = request.args.get('email')
    user = User.query.filter_by(email=email).first()
    if user:
        return {
            "code": 401,
            "message": "Email đã được sử dụng. Xin vui lòng chọn email khác!"
        }
    else:
        res = send_register_email(email)

    if res.status_code == 200:
        return {
            "code": 200,
            "message": f"Email xác nhận đã được gửi đến hòm thư {email} của bạn"
        }
    else:
        return {
            "code": 503,
            "message": "Đã có lỗi xảy ra khi gửi email. Vui lòng thử lại sau ít phút!"
        }

@app.route('/v1/api/login', methods=['POST'])
def login():
    payload = request.get_json()
    username = payload.get('username')
    password = payload.get('password')

    user = db.session.query(User).filter_by(username=username).first()
    if user:
        isCorrectPassword = user.check_password(password)
        if isCorrectPassword:
            token = jwt.encode(
                {
                    "id": user.id,
                },
                app.config['SECRET_KEY'],
                algorithm='HS256'
            )

            res = jsonify({
                "id": user.id,
                "name": user.name,
                "username": user.username
            })
            res.set_cookie(
                'access_token',
                value=token,
                max_age=60*60,
                httponly=True,
                secure=True,
                samesite=None
            )

            return res
    else:
        return {
            "code": 401,
            "message": "Sai tên đăng nhập hoặc mật khẩu"
        }