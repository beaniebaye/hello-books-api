from flask import Blueprint

hello_world_bp = Blueprint("hello_world", __name__)

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