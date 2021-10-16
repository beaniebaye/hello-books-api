from flask import Blueprint, jsonify

class Book:
    def __init__(self, id, title, description):
        self.id = id
        self.title = title
        self.description = description

books = [
    Book(1, "Fictional Book Title", "A fantasy novel set in an imaginary world."),
    Book(2, "Fictional Book Title", "A fantasy novel set in an imaginary world."),
    Book(3, "Fictional Book Title", "A fantasy novel set in an imaginary world.")
]


#Creates blueprints
hello_world_bp = Blueprint("hello_world", __name__)
books_bp = Blueprint("books", __name__, url_prefix="/books")


#Uses our books blueprint
@books_bp.route("", methods = ["GET"])
def handle_books():
    books_response = [
        {
            "id" : book.id,
            "title" : book.title,
            "description" : book.description
        } for book in books
    ]
    return jsonify(books_response)

@books_bp.route("/<book_id>", methods = ["GET"])
def handle_book(book_id):
    book_id = int(book_id)
    for book in books:
        if book.id == book_id:
            return {
                "id" : book.id,
                "title" : book.title,
                "description" : book.description
            }

#Uses our hello world blueprint
@hello_world_bp.route("/hello-world", methods = ["GET"])
def get_hello_world():
    response = "Hello World!"
    return response

@hello_world_bp.route("/hello-world/JSON", methods = ["GET"])
def hello_world_json():
    return {
        "name" : "Bean",
        "message" : "Let's get this bread",
        "hobbies" : ["Weightlifting", "Animal Crossing :)", "Roller skating"]
    }, 200

@hello_world_bp.route("/broken-endpoint-with-broken-server-code")
def broken_endpoint():
    response_body = {
        "name": "Ada Lovelace",
        "message": "Hello!",
        "hobbies": ["Fishing", "Swimming", "Watching Reality Shows"]
    }
    new_hobby = "Surfing"
    response_body["hobbies"].append(new_hobby)
    return response_body