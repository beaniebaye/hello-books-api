from app import db
from app.models.book import Book
from flask import Blueprint, jsonify, make_response, request



#Creates blueprints

books_bp = Blueprint("books", __name__, url_prefix="/books")

@books_bp.route("", methods=["GET","POST"])
def handle_books():

    if request.method == "GET":

        books = Book.query.all()

        response = []
        for book in books:
            response.append(
                {
                    "id" : book.id,
                    "title" : book.title,
                    "description" : book.description
                }
            )

        return jsonify(response)


    elif request.method == "POST":
        request_body = request.get_json()

        if "title" not in request_body or "description" not in request_body:
            return make_response("Invalid request", 400)

        new_book = Book(
            title=request_body["title"],
            description = request_body["description"]
        )

        db.session.add(new_book)
        db.session.commit()

        return make_response(f"Book {new_book.title} successfully created", 201)



@books_bp.route("/<book_id>", methods = ["GET", "PUT", "DELETE"])
def handle_book(book_id):

    book = Book.query.get(book_id)

    if book == None:
        return make_response("", 404)

    if request.method == "GET":

        return {
            "id" : book.id,
            "title" : book.title,
            "description" : book.description
        }

    elif request.method == "PUT":

        request_body = request.get_json()

        book.title = request_body["title"]
        book.description = request_body["description"]

        db.session.commit()

        return make_response(f"Book #{book_id} has successfully been updated")


    elif request.method == "DELETE":

        db.session.delete(book)
        db.session.commit()

        return make_response(f"Book #{book_id} successfully deleted")

