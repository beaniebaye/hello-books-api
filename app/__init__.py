from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from dotenv import load_dotenv
import os

db = SQLAlchemy()
migrate = Migrate()
load_dotenv()

# postgresql+psycopg2://postgres:postgres@localhost:5432/hello_books_development

def create_app(test_config=None):
    app = Flask(__name__)



    if not test_config:
        app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
        app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('SQLALCHEMY_DATABASE_URI')

    else:
        app.config["TESTING"] = True
        app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
        app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get(
            "SQLALCHEMY_TEST_DATABASE_URI")
        print("setting up test config")

    db.init_app(app)
    migrate.init_app(app, db)

    from app.models.book import Book
    from app.models.author import Author
    from app.models.genre import Genre
    from app.models.book_genre import BookGenre
    
    # register blueprints here

    from .routes import books_bp, authors_bp, genres_bp


    app.register_blueprint(books_bp)
    app.register_blueprint(authors_bp)
    app.register_blueprint(genres_bp)

    return app
