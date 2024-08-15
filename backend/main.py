import os
from flask import Flask, request, jsonify
from flask_restx import Api
from flask_migrate import Migrate
from flask_jwt_extended import JWTManager
from flask_cors import CORS
import requests
from exts import db
from config import Config

def create_app():
    app = Flask(__name__)

    app.config.from_object(Config)
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///dev.db"
    app.config['JWT_SECRET_KEY'] = 'your_secret_key'
    
    # The folder for storing images
    app.config['IMAGES_FOLDER'] = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'images')

    db.init_app(app)
    migrate = Migrate(app, db)
    jwt = JWTManager(app)

    # Enable CORS for the entire application
    CORS(app, resources={r"/*": {"origins": "http://localhost:3000"}})

    api = Api(app, doc='/docs')

    return app

app = create_app()

@app.route('/api/get_anime', methods=['GET'])
def get_anime():
    genre = request.args.get('genre')
    tag = request.args.get('tag')

    url = 'https://graphql.anilist.co'
    
    query = '''
    query ($genre: String, $tag: String, $page: Int, $perPage: Int) {
      Page(page: $page, perPage: $perPage) {
        pageInfo {
          total
          currentPage
          lastPage
          hasNextPage
        }
        media(genre: $genre, tag: $tag, type: ANIME, sort: [SCORE_DESC]) {
          id
          title {
            romaji
          }
          genres
          averageScore
          coverImage {
            large
          }
        }
      }
    }
    '''

    variables = {
        "genre": genre,
        "tag": tag,
        "page": 1,
        "perPage": 20  # Limit results to 20
    }

    response = requests.post(url, json={'query': query, 'variables': variables})
    
    if response.status_code == 200:
        data = response.json()['data']['Page']['media']
        return jsonify(data)
    else:
        return jsonify({"error": "Failed to fetch data from Anilist API"}), response.status_code

@app.shell_context_processor
def make_shell_context():
    return {
        "db": db,
    }

if __name__ == '__main__':
    app.run(debug=True)