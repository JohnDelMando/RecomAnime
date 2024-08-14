import os
from flask import Flask
from flask_restx import Api
from flask_migrate import Migrate
from flask_jwt_extended import JWTManager
from flask_cors import CORS
from exts import db
from config import Config

# from models import User

def create_app():
    app = Flask(__name__)


    app.config.from_object(Config)
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///dev.db"
    app.config['JWT_SECRET_KEY'] = 'your_secret_key'

    #the folder for storing the picture for the anime and its corresponding characters
    app.config['IMAGES_FOLDER'] = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'images')

    db.init_app(app)
    migrate = Migrate(app, db)
    jwt = JWTManager(app)

    # Enable CORS for the entire application
    CORS(app, resources={r"/*": {"origins": "http://localhost:3000"}})

    api = Api(app, doc='/docs')

    return app

app = create_app()

@app.shell_context_processor
def make_shell_context():
    return {
        "db": db,
        # "User": User
    }

if __name__ == '__main__':
    app.run(debug=True)