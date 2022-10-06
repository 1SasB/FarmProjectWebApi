
import jwt, os
# from dotenv import load_dotenv
from flask import Flask, request, jsonify, Blueprint
from api.save_image import save_pic_farm,save_pic_id,save_pic_progress
from api.validate import validate_project
import datetime
from flask_mail import Mail
from api.momo_api import api_user_id,user_key,get_token,request_to_pay
import uuid, ast,string,random

from api.models import FarmProject,Sponserd
from api.auth.auth_middleware import token_required

project = Blueprint(name="project",import_name=__name__,template_folder="templates")


def make_momo_api_call(x_Reference_Id,phone_numnber,amount):
    api_user_id(x_Reference_Id)
    api_user_key = user_key(x_Reference_Id)
    key = api_user_key.get('Data')
    print("User Key: ",key)
    gen_token = get_token(x_Reference_Id,key)
    auth_token = gen_token.get('Data')
    print("Token: ",auth_token)
    request_status = request_to_pay(x_Reference_Id,auth_token,phone_numnber,amount)
    print(str(request_status))
    return request_status



@project.route("/projects/", methods=["POST"])
@token_required
def create_project(current_user):
    try:
        project = dict(request.form)
        print(project)
        if not project:
            return {
                "message": "Invalid data, you need to give the project title, project image, user id,",
                "data": None,
                "error": "Bad Request"
            }, 400
        
        if not request.files["project_image"]:
            return {
                "message": "cover image is required",
                "data": None
            }, 400
        
        project["image_url"] = request.host_url+"static/images/farms/"+save_pic_farm(request.files["project_image"])
        
        is_validated = validate_project(**project)

        if is_validated is not True:
            return {
                "message": "Invalid data",
                "data": None,
                "error": is_validated
            }, 400
        project = FarmProject().create(**project, user_id=current_user["_id"])
        if not project:
            return {
                "message": "The project has been created by user",
                "data": None,
                "error": "Conflict"
            }, 400
        return jsonify({
            "message": "successfully created a new project",
            "data": project
        }), 201
    except Exception as e:
        return jsonify({
            "message": "failed to create a new project",
            "error": str(e),
            "data": None
        }), 500

@project.route("/user/projects/", methods=["GET"])
@token_required
def get_user_projects(current_user):
    try:
        projects = FarmProject().get_by_user_id(current_user["_id"])
        return jsonify({
            "message": "successfully retrieved all projects",
            "data": projects
        })
    except Exception as e:
        return jsonify({
            "message": "failed to retrieve all projects",
            "error": str(e),
            "data": None
        }), 500

@project.route("/projects/", methods=["GET"])
def get_projects():
    try:
        projects = FarmProject().get_all()
        return jsonify({
            "message": "successfully retrieved all projects",
            "data": projects
        }),200
    except Exception as e:
        return jsonify({
            "message": "failed to retrieve all projects",
            "error": str(e),
            "data": None
        }), 500

@project.route("/projects/<project_id>", methods=["GET"])
@token_required
def get_project(current_user,project_id):
    try:
        project = FarmProject().get_by_id(project_id)
        if not project:
            return {
                "message": "project not found",
                "data": None,
                "error": "Not Found"
            }, 404
        return jsonify({
            "message": "successfully retrieved a project",
            "data": project
        })
    except Exception as e:
        return jsonify({
            "message": "Something went wrong",
            "error": str(e),
            "data": None
        }), 500

@project.route("/projects/<project_id>", methods=["PUT"])
@token_required
def update_project(current_user, project_id):
    print("here")
    try:
        print("here")
        project = FarmProject().get_by_id(project_id)
        print(project)
        if not project or project["user_id"] != current_user["_id"]:
            return {
                "message": "project not found for user",
                "data": None,
                "error": "Not found"
            }, 404
        project = request.form
        print(project)
        if project.get('project_image'):
            project["image_url"] = request.host_url+"static/images/farms/"+save_pic_farm(request.files["cover_image"])
        project = FarmProject().update(project_id, dict(project))
        return jsonify({
            "message": "successfully updated a project",
            "data": project
        }), 201
    except Exception as e:
        return jsonify({
            "message": "failed to update a project",
            "error": str(e),
            "data": None
        }), 400

@project.route("/sponserproject/", methods=["POST"])
@token_required
def sponser_project(current_user):
    try:
        print("inside soonser project")
        content = dict(request.form)
        # project_id = content.get("project_id")
        # print(current_user)

        data = Sponserd().create(current_user.get("_id"),**content)
        print("crerated project")
        if not data:
            return {
                "message": "Couldnt create add sponser",
                "error": "Conflict",
                "data": None
            }, 400
        return {
            "message": "Successfully Added sponsor to project",
            "data": data
        }, 201
    except Exception as e:
        print(e)
        return {
            "message": "Something went wrong",
            "error": str(e),
            "data": None
        }, 500

@project.route("/sponserproject/update/<spons_id>", methods=["POST"])
@token_required
def update_sponser_project(current_user,spons_id):
    try:
        print("inside update soonser project")
        content = dict(request.form)
        # project_id = content.get("project_id")
        # print(current_user)

        data = Sponserd().update(spons_id,content)
        print("crerated project")
        if not data:
            return {
                "message": "Couldnt Update sponsered",
                "error": "Conflict",
                "data": None
            }, 400
        return {
            "message": "Successfully Updated sponsored project",
            "data": data
        }, 201
    except Exception as e:
        print(e)
        return {
            "message": "Something went wrong",
            "error": str(e),
            "data": None
        }, 500


@project.route("/user/sponserd", methods=["GET"])
@token_required
def sponsord(current_user):
    try:
        data = Sponserd().get_by_user_id(current_user.get("_id"))
        return {
           "message": "Successfully Got sponse",
            "data": data
        }, 200
    except Exception as e:
        print(e)
        return {
            "message": "Something went wrong",
            "error": str(e),
            "data": None
        }, 500

@project.route("/pay-sponser/<sponsered_id>", methods=["POST"])
@token_required
def pay_sponsord(current_user,sponsered_id):
    try:
        data = Sponserd().get_by_id(sponsered_id)
        print(data)
        x_Reference_Id =  str(uuid.uuid4())
        request_status = make_momo_api_call(x_Reference_Id,current_user.get("phone"),float(data.get("total_amount")))
        if str(request_status) == "202":
            data = Sponserd().pay(sponsered_id)
            return {
                "message": "Success",
                "data": data
            }, 200
        else:
            return{
                "message": "Payment Unsuccessful",
                "data": None
            },400
    except Exception as e:
        return {
            "message": "Something went wrong",
            "error": str(e),
            "data": None
        }, 500

@project.route("/sponserd/<sponsered_id>", methods=["GET"])
@token_required
def get_sponsord(current_user,sponsered_id):
    try:
        data = Sponserd().get_by_id(sponsered_id)
        return {
           "message": "Successfully Got sponsered Project",
            "data": data
        }, 200
    except Exception as e:
        return {
            "message": "Something went wrong",
            "error": str(e),
            "data": None
        }, 500

@project.route("/sponserd/update-progress/<sponsered_id>", methods=["POST"])
@token_required
def update_progress(current_user,sponsered_id):
    try:
        dta = dict(request.form)
        files = dict(request.files)
        print(dta)
        print(files)
        dta["st1_image_url1"] = request.host_url+"static/images/farms/"+save_pic_progress(files["stage_image1"])
        dta["st1_image_url2"] = request.host_url+"static/images/farms/"+save_pic_progress(files["stage_image2"])
        dta["st2_image_url1"] = request.host_url+"static/images/farms/"+save_pic_progress(files["stage_image3"])
        dta["st2_image_url2"] = request.host_url+"static/images/farms/"+save_pic_progress(files["stage_image4"])

        data = Sponserd().update_progress(sponsered_id,dta)
        return {
           "message": "Successfully Got sponsered Project",
            "data": data
        }, 201
    except Exception as e:
        return {
            "message": "Something went wrong",
            "error": str(e),
            "data": None
        }, 500


@project.route("/projects/<project_id>", methods=["DELETE"])
@token_required
def delete_project(current_user, project_id):
    try:
        project = FarmProject().get_by_id(project_id)
        if not project or project["user_id"] != current_user["_id"]:
            return {
                "message": "project not found for user",
                "data": None,
                "error": "Not found"
            }, 404
        FarmProject().delete(project_id)
        return jsonify({
            "message": "successfully deleted a project",
            "data": None
        }), 204
    except Exception as e:
        return jsonify({
            "message": "failed to delete a project",
            "error": str(e),
            "data": None
        }), 400