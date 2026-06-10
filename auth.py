from flask import Blueprint, request

auth = Blueprint("auth", __name__)

USERNAME = "mother"

PASSWORD = "lic123"

@auth.route("/login", methods=["POST"])
def login():

    data = request.json

    username = data["username"]
    password = data["password"]

    if (
        username == USERNAME
        and password == PASSWORD
    ):
        return {
            "success": True
        }

    return {
        "success": False
    }, 401