import jwt, os
# from dotenv import load_dotenv
from flask import request, jsonify,url_for,render_template,current_app, Blueprint
from api.save_image import save_pic_farm,save_pic_id
from api.validate import validate_email_and_password, validate_user,validate_user_profile
import datetime
from flask_mail import Mail
from api.auth.conf_email import send_conf_email


from api.models import User
from api.auth.auth_middleware import token_required
from api.auth.token import generate_confirmation_token,confirm_token


auth = Blueprint(name="auth",import_name=__name__,template_folder="templates")

@auth.route("/users/", methods=["POST"])
def add_user():
    try:
        user = request.json
        print(user)

        if not user:
            return {
                "message": "Please provide user details",
                "data": None,
                "error": "Bad request"
            }, 400
        is_validated = validate_user(**user)
        if is_validated is not True:
            return dict(message='Invalid data', data=None, error=is_validated), 400
        user = User().create(**user)
        if not user:
            return {
                "message": "User already exists",
                "error": "Conflict",
                "data": None
            }, 409
        print("passed here")
        confirmation_token = generate_confirmation_token(user.get("email"))
        print("generated confirmation token")
        confirm_url = url_for('auth.confirm_email', token=confirmation_token, _external=True)
        print("generated confirmation email link")
        html = render_template('activate.html', confirm_url=confirm_url)
        print("generated confirmation email")
        subject = "Please Confirm Your email"
        send_conf_email(user.get("email"), subject, html)
        return {
            "message": "Successfully created new user",
            "data": user
        }, 201
    except Exception as e:
        return {
            "message": "Something went wrong",
            "error": str(e),
            "data": None
        }, 500


@auth.route('/resend-confirmation', methods=["POST"])
@token_required
def resend_confirmation(current_user):
    token = generate_confirmation_token(current_user.email)
    confirm_url = url_for('confirm_email', token=token, _external=True)
    html = render_template('activate.html', confirm_url=confirm_url)
    subject = "Please confirm your email"
    send_conf_email(current_user.email, subject, html)
    return{
        "message" : "Successfully sent confirmation email"
    }


@auth.route('/confirm-email/<token>', methods=["POST","GET"])
def confirm_email(token):
    print("about to confirm token")
    try:
        email = confirm_token(token)
    except Exception as e:
        print()
        return '<h1>The confirmation link is invalid or has expired</h1>'
    user = User().get_by_email(email)
    if user.get('confirmed'):
        return '<h1>Account already confirmed. Please login.</h1>'
    else:
        user = User().update(user.get('_id'),{
            "confirmed": True,
            "confirmed_on": datetime.datetime.now()
        })
        if not user:
            return{
                "message": "Couldnt confirm account"
            }, 500
        return '<h1>Email Confirmation successful</h1>'



@auth.route("/users/create-profile", methods=["POST"])
@token_required
def create_user_profile(current_user):
    try:
        profile = dict(request.form)
        if not profile:
            return {
                "message": "Please provide profile details",
                "data": None,
                "error": "Bad request"
            }, 400
        is_validated = validate_user_profile(**profile)
        profile["id_photo_url"] = request.host_url+"static/images/id/"+save_pic_id(request.files["id_photo"])
        if is_validated is not True:
            return dict(message='Invalid data', data=None, error=is_validated), 400
        user = User().create_profile(current_user["_id"],**profile)
        if not user:
            return {
                "message": "Couldnt create user pofile",
                "error": "Conflict",
                "data": None
            }, 409
        return {
            "message": "Successfully add user profile",
            "data": user
        }, 201
    except Exception as e:
        return {
            "message": "Something went wrong",
            "error": str(e),
            "data": None
        }, 500



@auth.route("/users/login/", methods=["POST"])
def login():
    try:
        data = request.json
        if not data:
            return {
                "message": "Please provide user details",
                "data": None,
                "error": "Bad request"
            }, 400
        # validate input
        is_validated = validate_email_and_password(data.get('email'), data.get('password'))
        if is_validated is not True:
            return dict(message='Invalid data', data=None, error=is_validated), 400
        user = User().login(
            data["email"],
            data["password"]
        )
        if user:
            try:
                # token should expire after 24 hrs
                user["token"] = jwt.encode(
                    {"user_id": user["_id"]},
                    current_app.config["SECRET_KEY"],
                    algorithm="HS256"
                )
                return {
                    "message": "Successfully fetched auth token",
                    "data": user
                }, 200
            except Exception as e:
                return {
                    "error": "Something went wrong",
                    "message": str(e)
                }, 500
        return {
            "message": "Error fetching auth token!, invalid email or password",
            "data": None,
            "error": "Unauthorized"
        }, 404
    except Exception as e:
        return {
                "message": "Something went wrong!",
                "error": str(e),
                "data": None
        }, 500



@auth.route("/users/", methods=["GET"])
@token_required
def get_current_user(current_user):
    print(current_user)
    return jsonify({
        "message": "successfully retrieved user profile",
        "data": current_user
    }),200



@auth.route("/users/", methods=["PUT"])
@token_required
def update_user(current_user):
    try:
        print("here")
        print(request.files)
        print(request.form)
        user = dict(request.form)
        print(user)
        if user:
            user["id_photo_url"] = request.host_url+"static/images/id/"+save_pic_id(request.files["id_photo"])
            user = User().update(current_user["_id"], user)
            return jsonify({
                "message": "successfully updated account",
                "data": user
            }), 201
        return {
            "message": "Invalid data!",
            "data": None,
            "error": "Bad Request"
        }, 400
    except Exception as e:
        return jsonify({
            "message": "failed to update account",
            "error": str(e),
            "data": None
        }), 400


@auth.route("/users/", methods=["DELETE"])
@token_required
def disable_user(current_user):
    try:
        User().disable_account(current_user["_id"])
        return jsonify({
            "message": "successfully disabled acount",
            "data": None
        }), 204
    except Exception as e:
        return jsonify({
            "message": "failed to disable account",
            "error": str(e),
            "data": None
        }), 400
