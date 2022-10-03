import jwt, os
# from dotenv import load_dotenv
from flask import Flask, request, jsonify,url_for,render_template,current_app
from api.save_image import save_pic
from api.validate import validate_project, validate_email_and_password, validate_user,validate_user_profile
import datetime
from flask_mail import Mail
from api.conf_email import send_conf_email

# load_dotenv()

# app = Flask(__name__)
# mail = Mail(app)


# if __name__ == "__main__":
#     app.run(debug=True)
