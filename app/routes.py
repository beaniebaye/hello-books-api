from flask import Blueprint, jsonify



#Creates blueprints

books_bp = Blueprint("books", __name__, url_prefix="/books")


#Uses our books blueprint
# @books_bp.route("", methods = ["GET"])
# def handle_books():
#     books_response = [
#         {
#             "id" : book.id,
#             "title" : book.title,
#             "description" : book.description
#         } for book in books
#     ]
#     return jsonify(books_response)

# @books_bp.route("/<book_id>", methods = ["GET"])
# def handle_book(book_id):
#     book_id = int(book_id)
#     for book in books:
#         if book.id == book_id:
#             return {
#                 "id" : book.id,
#                 "title" : book.title,
#                 "description" : book.description
#             }

