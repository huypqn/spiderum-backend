import jwt
from time import time
from app import app

def get_register_token(email, expires_in=1800):
    return jwt.encode(
        {
            "email": email,
            'exp': time() + expires_in,
        },
        app.config['SECRET_KEY'],
        algorithm='HS256'
    )

def verify_register_token(token):
    try:
        email = jwt.decode(
            token,
            app.config['SECRET_KEY'],
            algorithms=['HS256']
        )['email']
    except:
        return {
            "code": 401,
            "message": "Có lỗi xảy ra. Xin vui lòng thử lại sau!"
        }
    
    return {
        "code": 200,
        "email": email
    }