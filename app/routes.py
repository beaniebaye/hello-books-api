from app import db
from app.models.book import Book
from app.models.author import Author
from app.models.genre import Genre
from flask import Blueprint, jsonify, make_response, request, abort

#Creates blueprints

books_bp = Blueprint("books", __name__, url_prefix="/books")

authors_bp = Blueprint("authors", __name__, url_prefix="/authors")

genres_bp = Blueprint("genres", __name__, url_prefix="/genres")


# Helper Functions

def valid_int(number, parameter_type):
    try:
        int(number)
    except:
        abort(make_response({"error": f"{parameter_type} must be an int"}, 400))

def get_book_from_id(book_id):
    valid_int(book_id, "book_id")
    return Book.query.get_or_404(book_id, description="{book not found}")

def get_author_from_id(author_id):
    valid_int(author_id, "author_id")
    return Author.query.get_or_404(author_id, description="{author not found}")

# Author Routes

@authors_bp.route("", methods=["GET"])
def read_all_authors():

    authors = Author.query.all()

    authors_response = [author.to_dict for author in authors]

    return jsonify(authors_response)

@authors_bp.route("", methods=["POST"])
def create_author():

    request_body = request.get_json()

    if "name" not in request_body:
        return make_response("Invalid request", 400)

    new_author = Author(
            name=request_body["name"]
        )

    return new_author.to_dict(), 201


# Book Routes

@books_bp.route("", methods=["GET"])
def read_all_books():

    title_query = request.args.get("title")

    if title_query:
        books = Book.query.filter_by(title=title_query)
    else:
        books = Book.query.all()

    books_response = [book.to_dict() for book in books]

    return jsonify(books_response)


@books_bp.route("", methods=["POST"])
def create_book():

    request_body = request.get_json()

    if "title" not in request_body or "description" not in request_body:
        return make_response("Invalid request", 400)

    new_book = Book(
        title=request_body["title"],
        description = request_body["description"]
        )

    db.session.add(new_book)
    db.session.commit()

    return new_book.to_dict(), 201
    

@books_bp.route("/<book_id>", methods = ["GET"])
def read_one_book(book_id):
    book = get_book_from_id(book_id)

    return book.to_dict()

@books_bp.route("/<book_id>", methods = ["PUT"])
def update_one_book(book_id):
    book = get_book_from_id(book_id)

    request_body = request.get_json()

    if "title" in request_body:
        book.title = request_body["title"]
    if "description" in request_body:
        book.description = request_body["description"]

    db.session.commit()

    return jsonify(book.to_dict)

@books_bp.route("/<book_id>", methods = ["DELETE"])
def delete_one_book(book_id):
    book = get_book_from_id(book_id)

    db.session.delete(book)
    db.session.commit()

    return make_response(f"Book #{book_id} successfully deleted")

# Nested Routes

@authors_bp.route("/<author_id>/books", methods=["POST"])
def create_book_for_author(author_id):

    author = get_author_from_id(author_id)

    request_body = request.get_json()

    new_book = Book(
        title=request_body["title"],
        description=request["description"],
        author=author
    )

    db.session.add(new_book)
    db.session.commit()

    return make_response(f"Book {new_book.title} by {new_book.author.name} successfully created", 201)

@authors_bp.route("/<author_id>/books", methods=["POST"])
def read_all_books_from_one_author(author_id):

    author = get_author_from_id(author_id)

    books_response = [book.to_dict for book in author.books]

    return jsonify(books_response)

# genre routes

@genres_bp.route("", methods=["GET"])
def read_all_genres():
    genres = Genre.query.all()

    response_body = [genre.to_dict for genre in genres]

    return jsonify(response_body)

@genres_bp.route("", methods=["POST"])
def create_genre():
    request_body = request.get_json()

    genre = Genre(name=request_body["name"])

    db.session.add(genre)
    db.session.commit()

    return jsonify(f"Genre {genre.name} was successfully created"), 201

# Nested routes for books and genre

@books_bp.route("/<book_id>/assign_genres", methods=["PATCH"])
def assign_genres(book_id):
    book = Book.query.get(book_id)

    if book is None:
        return make_response(f"Book #{book.id} not found", 404)
  
    request_body = request.get_json()

    for id in request_body["genres"]:
        book.genres.append(Genre.query.get(id))
  
    db.session.commit()

    return make_response("Genres successfully added", 200)

