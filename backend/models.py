from exts import db

# Association table for anime genres
anime_genres = db.Table(
    'anime_genres',
    db.Column('anime_id', db.Integer, db.ForeignKey('anime.anime_id'), primary_key=True),
    db.Column('genre_id', db.Integer, db.ForeignKey('genre.genre_id'), primary_key=True)
)

# Association table for anime tags
anime_tags = db.Table(
    'anime_tags',
    db.Column('anime_id', db.Integer, db.ForeignKey('anime.anime_id'), primary_key=True),
    db.Column('tag_id', db.Integer, db.ForeignKey('tag.tag_id'), primary_key=True)
)

# Anime table
class Anime(db.Model):
    __tablename__ = 'anime'
    
    anime_id = db.Column(db.Integer, primary_key=True)
    anime_name = db.Column(db.String(100), nullable=False, unique=True, index=True)
    anime_description = db.Column(db.Text, nullable=True)
    anime_image = db.Column(db.String, nullable=True)
    anime_studio = db.Column(db.String, nullable=True)
    number_of_episodes = db.Column(db.Integer, nullable=True)
    anime_type = db.Column(db.String, nullable=True)
    anime_status = db.Column(db.String, nullable=True)
    anime_rating = db.Column(db.Float, nullable=True)
    anime_score = db.Column(db.Float, nullable=True)

    characters = db.relationship('Character', backref='anime', lazy=True)
    genres = db.relationship('Genre', secondary=anime_genres, lazy='subquery', backref=db.backref('animes', lazy=True))
    tags = db.relationship('Tag', secondary=anime_tags, lazy='subquery', backref=db.backref('animes', lazy=True))
    
    def __repr__(self):
        return f"<Anime {self.anime_name}>"

    def save(self):
        db.session.add(self)
        db.session.commit()

    def serialize(self):
        return {
            'anime_id': self.anime_id,
            'anime_name': self.anime_name,
            'anime_description': self.anime_description,
            'anime_image': self.anime_image,
            'anime_studio': self.anime_studio,
            'number_of_episodes': self.number_of_episodes,
            'anime_type': self.anime_type,
            'anime_status': self.anime_status,
            'anime_rating': self.anime_rating,
            'anime_score': self.anime_score,
            'genres': [genre.serialize() for genre in self.genres],
            'tags': [tag.serialize() for tag in self.tags]
        }

# Character table
class Character(db.Model):
    __tablename__ = 'character'
    
    character_id = db.Column(db.Integer, primary_key=True)
    character_name = db.Column(db.String(100), nullable=False, index=True)
    character_image = db.Column(db.String, nullable=True)
    anime_id = db.Column(db.Integer, db.ForeignKey('anime.anime_id'), nullable=False)

    def __repr__(self):
        return f"<Character {self.character_name}>"

    def save(self):
        db.session.add(self)
        db.session.commit()

    def serialize(self):
        return {
            'character_id': self.character_id,
            'character_name': self.character_name,
            'character_image': self.character_image,
            'anime_id': self.anime_id
        }

# Genre table
class Genre(db.Model):
    __tablename__ = 'genre'
    
    genre_id = db.Column(db.Integer, primary_key=True)
    genre_name = db.Column(db.String(50), nullable=False, unique=True)

    def __repr__(self):
        return f"<Genre {self.genre_name}>"

    def save(self):
        db.session.add(self)
        db.session.commit()

    def serialize(self):
        return {
            'genre_id': self.genre_id,
            'genre_name': self.genre_name
        }

# Tag table (formerly Theme table)
class Tag(db.Model):
    __tablename__ = 'tag'
    
    tag_id = db.Column(db.Integer, primary_key=True)
    tag_name = db.Column(db.String(50), nullable=False, unique=True)

    def __repr__(self):
        return f"<Tag {self.tag_name}>"

    def save(self):
        db.session.add(self)
        db.session.commit()

    def serialize(self):
        return {
            'tag_id': self.tag_id,
            'tag_name': self.tag_name
        }

# Date table
class Date(db.Model):
    __tablename__ = 'date'
    
    date_id = db.Column(db.Integer, primary_key=True)
    date_premiere = db.Column(db.Date, nullable=True)
    date_start = db.Column(db.Date, nullable=True)
    date_end = db.Column(db.Date, nullable=True)

    def __repr__(self):
        return f"<Date {self.date_id}>"

    def save(self):
        db.session.add(self)
        db.session.commit()

    def serialize(self):
        return {
            'date_id': self.date_id,
            'date_premiere': self.date_premiere,
            'date_start': self.date_start,
            'date_end': self.date_end
        }

# TopAnime table
class TopAnime(db.Model):
    __tablename__ = 'top_anime'
    
    top_anime_id = db.Column(db.Integer, primary_key=True)
    top_anime_name = db.Column(db.String(100), nullable=False, unique=True)

    def __repr__(self):
        return f"<TopAnime {self.top_anime_name}>"

    def save(self):
        db.session.add(self)
        db.session.commit()

    def serialize(self):
        return {
            'top_anime_id': self.top_anime_id,
            'top_anime_name': self.top_anime_name
        }