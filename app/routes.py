from flask import request, redirect
from app import app
from app.email import send_register_email
from app.models import User


@app.route('/register', methods=['GET', 'POST'])
def register():
    email = request.args.get('email')
    user = User.query.filter_by(email=email).first()
    if user:
        return {
            "code": 401,
            "message": "Người dùng đã tồn tại. Vui lòng nhập Email khác!"
        }
    else:
        send_register_email(email)

    return {
        "code": 200,
        "message": "Email xác nhận đã được gửi đến hòm thư pqh.one@gmail.com của bạn"
    }

