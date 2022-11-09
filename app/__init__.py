from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_restful import Api
from flask_mail import Mail
from flask_cors import CORS
from config import Config


app = Flask(__name__)
app.config.from_object(Config)
db = SQLAlchemy(app)
migrate = Migrate(app, db)
api = Api(app)
cors = CORS(app)
mail = Mail(app)

from app import routes, models, api_module, services

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)