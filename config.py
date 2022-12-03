import os
import secrets

baseDir = os.path.abspath(os.path.dirname(__name__))

class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY') or secrets.token_hex(16)
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'sqlite:///' + os.path.join(baseDir, 'spiderum.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SESSION_COOKIE_SAMESITE = 'None'
    SESSION_COOKIE_SECURE = True
    POSTS_PER_PAGE = 10

    WEBSITE_URI = "https://clospider.vercel.app"
    API_KEY = "e0f03f09b01086fb5c7ce6632ffe11fd"
    API_SECRET = "5817357399d100ff4d65476ffd384b1f"
    NOREPLY = 'spidermannoreply@gmail.com'