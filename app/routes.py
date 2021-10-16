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