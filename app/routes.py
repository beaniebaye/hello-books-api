from app import db
from app.models.book import Book
from app.models.author import Author
from flask import Blueprint, jsonify, make_response, request, abort



#Creates blueprints

books_bp = Blueprint("books", __name__, url_prefix="/books")

authors_bp = Blueprint("authors", __name__, url_prefix="/authors")


# Helper Functions

def valid_int(number, parameter_type):
    try:
        int(number)
    except:
        abort(make_response({"error": f"{parameter_type} must be an int"}, 400))

def get_book_from_id(book_id):
    valid_int(book_id, "book_id")
    return Book.query.get_or_404(book_id, description="{book not found}")

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