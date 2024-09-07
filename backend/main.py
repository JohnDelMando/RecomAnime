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



#get top anime with specified genre and tag
@app.route('/api/get_topAnime', methods=['GET'])
def get_topAnime():
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
    


# get most popular anime that is releasing in the year, year is hardcoded for now
@app.route('/api/get_popularAnime', methods=['GET'])
def get_popularAnime():
    url = 'https://graphql.anilist.co'
    
    query = '''
    query ($page: Int, $perPage: Int) {
      Page(page: $page, perPage: $perPage) {
        media(type: ANIME, sort: [POPULARITY_DESC], seasonYear: 2024, status: RELEASING) {
          id
          title {
            romaji
          }
          popularity
          coverImage {
            large
          }
        }
      }
    }
    '''

    variables = {
        "page": 1,
        "perPage": 20  # Limit results to 20
    }

    response = requests.post(url, json={'query': query, 'variables': variables})
    
    if response.status_code == 200:
        data = response.json()['data']['Page']['media']
        return jsonify(data)
    else:
        return jsonify({"error": "Failed to fetch data from Anilist API"}), response.status_code
    


# get anime airing with specific season and year (inputs are: WINTER, FALL, SUMMER, SPRING)
@app.route('/api/get_seasonalAnime', methods=['GET'])
def get_seasonalAnime():
    season = request.args.get('season')
    year = request.args.get('year')

    url = 'https://graphql.anilist.co'
    
    query = '''
    query ($season: MediaSeason, $year: Int, $page: Int, $perPage: Int) {
      Page(page: $page, perPage: $perPage) {
        media(season: $season, seasonYear: $year, type: ANIME) {
          id
          title {
            romaji
          }
          coverImage {
            large
          }
        }
      }
    }
    '''

    variables = {
        "season": season,  # WINTER, FALL, SUMMER, SPRING
        "year": int(year),  
        "page": 1,
        "perPage": 50 # Limit results to 50
    }

    response = requests.post(url, json={'query': query, 'variables': variables})
    
    if response.status_code == 200:
        data = response.json()['data']['Page']['media']
        return jsonify(data)
    else:
        return jsonify({"error": "Failed to fetch data from Anilist API"}), response.status_code
    


#Get the anime with specific genre
@app.route('/api/get_genreAnime', methods=['GET'])
def get_genreAnime():
    genre = request.args.get('genre')

    url = 'https://graphql.anilist.co'
    
    query = '''
    query ($genre: String, $page: Int, $perPage: Int) {
      Page(page: $page, perPage: $perPage) {
        media(genre: $genre, type: ANIME, sort: [POPULARITY_DESC, SCORE_DESC]) {
          id
          title {
            romaji
          }
          genres
          averageScore
          popularity
          coverImage {
            large
          }
        }
      }
    }
    '''

    variables = {
        "genre": genre,
        "page": 1,
        "perPage": 25  # Limit results to top 25
    }

    response = requests.post(url, json={'query': query, 'variables': variables})
    
    if response.status_code == 200:
        data = response.json()['data']['Page']['media']
        return jsonify(data)
    else:
        return jsonify({"error": "Failed to fetch data from Anilist API"}), response.status_code

    

#Get the anime with specific tag
@app.route('/api/get_tagAnime', methods=['GET'])
def get_tagAnime():
    tag = request.args.get('tag')

    url = 'https://graphql.anilist.co'
    
    query = '''
    query ($tag: String, $page: Int, $perPage: Int) {
      Page(page: $page, perPage: $perPage) {
        media(tag: $tag, type: ANIME, sort: [POPULARITY_DESC, SCORE_DESC]) {
          id
          title {
            romaji
          }
          tags {
            name
          }
          averageScore
          popularity
          coverImage {
            large
          }
        }
      }
    }
    '''

    variables = {
        "tag": tag,
        "page": 1,
        "perPage": 25  # Limit results to top 25
    }

    response = requests.post(url, json={'query': query, 'variables': variables})
    
    if response.status_code == 200:
        data = response.json()['data']['Page']['media']
        return jsonify(data)
    else:
        return jsonify({"error": "Failed to fetch data from Anilist API"}), response.status_code
    


# get top anime with multiple value for genre. Example: Genre = Action, Adventure, Fantasy. Postman request URL: ?genre=Action,Fantasy,Adventure
@app.route('/api/get_multgenreAnime', methods=['GET'])
def get_multgenreAnime():
    genre_list = request.args.get('genre').split(',')

    url = 'https://graphql.anilist.co'
    
    query = '''
    query ($genre_in: [String], $page: Int, $perPage: Int) {
      Page(page: $page, perPage: $perPage) {
        media(genre_in: $genre_in, type: ANIME, sort: [POPULARITY_DESC, SCORE_DESC]) {
          id
          title {
            romaji
          }
          genres
          averageScore
          popularity
          coverImage {
            large
          }
        }
      }
    }
    '''

    variables = {
        "genre_in": genre_list,  # Pass the list of genres
        "page": 1,
        "perPage": 25  # Limit results to top 25
    }

    response = requests.post(url, json={'query': query, 'variables': variables})
    
    if response.status_code == 200:
        data = response.json()['data']['Page']['media']
        return jsonify(data)
    else:
        return jsonify({"error": "Failed to fetch data from Anilist API"}), response.status_code



# get top anime with multiple value for tag. Example: Tag = Shounen, Super Power. Postman request URL: ?tag=Shounen,Super Power
@app.route('/api/get_multtagAnime', methods=['GET'])
def get_multtagAnime():
    tag_list = request.args.get('tag').split(',')

    url = 'https://graphql.anilist.co'
    
    query = '''
    query ($tag_in: [String], $page: Int, $perPage: Int) {
      Page(page: $page, perPage: $perPage) {
        media(tag_in: $tag_in, type: ANIME, sort: [POPULARITY_DESC, SCORE_DESC]) {
          id
          title {
            romaji
          }
          tags {
            name
          }
          averageScore
          popularity
          coverImage {
            large
          }
        }
      }
    }
    '''

    variables = {
        "tag_in": tag_list,  # Pass the list of tags
        "page": 1,
        "perPage": 25  # Limit results to top 25
    }

    response = requests.post(url, json={'query': query, 'variables': variables})
    
    if response.status_code == 200:
        data = response.json()['data']['Page']['media']
        return jsonify(data)
    else:
        return jsonify({"error": "Failed to fetch data from Anilist API"}), response.status_code
    


# get the top anime of the year
@app.route('/api/get_yearlyAnime', methods=['GET'])
def get_yearlyAnime():
    year = request.args.get('year')

    url = 'https://graphql.anilist.co'
    
    query = '''
    query ($year: Int, $page: Int, $perPage: Int) {
      Page(page: $page, perPage: $perPage) {
        media(seasonYear: $year, type: ANIME, sort: [POPULARITY_DESC, SCORE_DESC]) {
          id
          title {
            romaji
          }
          averageScore
          popularity
          coverImage {
            large
          }
        }
      }
    }
    '''

    variables = {
        "year": int(year), 
        "page": 1,
        "perPage": 50  # Limit results to top 50
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