from flask import request
from app import app
from app.models import User
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
            "code": 401,
            "message": "Đã có lỗi xảy ra khi gửi email. Vui lòng thử lại sau ít phút!"
        }