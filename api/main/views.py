import jwt, os
# from dotenv import load_dotenv
from flask import Flask, request, jsonify,current_app, Blueprint




main = Blueprint(name="main",import_name=__name__,template_folder="templates")




@main.route("/")
def hello():
    return "Farm Project Backend"



@current_app.errorhandler(403)
def forbidden(e):
    return jsonify({
        "message": "Forbidden",
        "error": str(e),
        "data": None
    }), 403

@current_app.errorhandler(404)
def forbidden(e):
    return jsonify({
        "message": "Endpoint Not Found",
        "error": str(e),
        "data": None
    }), 404
