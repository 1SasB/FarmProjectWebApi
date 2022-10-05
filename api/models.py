"""Application Models"""
from datetime import datetime
import bson, os
from api import mongo
from dotenv import load_dotenv
# from pymongo import MongoClient
from werkzeug.security import generate_password_hash, check_password_hash

# load_dotenv()

# DATABASE_URL=os.environ.get('DATABASE_URL') or 'mongodb://localhost:27017/FarmDatabase'
# print(DATABASE_URL)
# # client = MongoClient(DATABASE_URL)
db = mongo.db

class FarmProject:
    """Farm Project Model"""
    def __init__(self):
        return

    def create(self, title="", description="", image_url="", product="", user_id="",resources="",cost_per_unit="",start_date="",end_date="",available_slots="",ROS=""):
        """Create a new Farm Project"""
        project = self.get_by_user_id_and_title(user_id, title)
        if project:
            return
        new_project = db.projects.insert_one(
            {
                "title": title,
                "description": description,
                "image_url": image_url,
                "product": product,
                "user_id": user_id,
                "resources": resources,
                "status": "upcoming",
                "cost_per_unit": cost_per_unit,
                "start_date": start_date,
                "end_date": end_date,
                "available_slot": available_slots,
                "ROS" :ROS

            }
        )
        return self.get_by_id(new_project.inserted_id)

    def get_all(self):
        """Get all Farm Project"""
        projects = db.projects.find()
        return [{**project, "_id": str(project["_id"])} for project in projects]

    def get_by_id(self, project_id):
        """Get a project by id"""
        project = db.projects.find_one({"_id": bson.ObjectId(project_id)})
        if not project:
            return
        project["_id"] = str(project["_id"])
        return project

    def get_by_user_id(self, user_id):
        """Get all project created by a user"""
        projects = db.projects.find({"user_id": user_id})
        return [{**project, "_id": str(project["_id"])} for project in projects]
       
    def get_by_product(self, product):
        """Get all project by product"""
        projects = db.projects.find({"product": product})
        return [project for project in projects]

    def get_by_user_id_and_product(self, user_id, product):
        """Get all project by category for a particular user"""
        projects = db.projects.find({"user_id": user_id, "product": product})
        return [{**project, "_id": str(project["_id"])} for project in projects]

    def get_by_user_id_and_title(self, user_id, title):
        """Get a project given its title and author"""
        project = db.projects.find_one({"user_id": user_id, "title": title})
        if not project:
            return
        project["_id"] = str(project["_id"])
        return project

    def update(self, project_id, data):
        """Update a project"""
        # data={}
        # if title: data["title"]=title
        # if description: data["description"]=description
        # if image_url: data["image_url"]=image_url
        # if product: data["category"]=product

        allowed_keys = ["title","desciption","image_url","product","cost_per_unit","resources","start_date","end_date","ROS","available_slots"]
        ndata = {}
        for i in data.keys():
            if i in allowed_keys:
                ndata[i] = data[i]

        # user = db.users.update_one(
        #     {"_id": bson.ObjectId(user_id)},
        #     {
        #         "$set": ndata
        #     }
        # )
        # user = self.get_by_id(user_id)
        # return user

        project = db.projects.update_one(
            {"_id": bson.ObjectId(project_id)},
            {
                "$set": ndata
            }
        )
        project = self.get_by_id(project_id)
        return project

    def delete(self, project_id):
        """Delete a project"""
        project = db.projects.delete_one({"_id": bson.ObjectId(project_id)})
        return project

    def delete_by_user_id(self, user_id):
        """Delete all projects created by a user"""
        project = db.projects.delete_many({"user_id": bson.ObjectId(user_id)})
        return project


class User:
    """User Model"""
    def __init__(self):
        return

    def create(self, name="", email="", password=""):
        """Create a new user"""
        user = self.get_by_email(email)
        if user:
            return
        new_user = db.users.insert_one(
            {
                "name": name,
                "email": email,
                "password": self.encrypt_password(password),
                "active": True,
                "confirmed": False,
                "profile_completed": False
            }
        )
        return self.get_by_id(new_user.inserted_id)

    def create_profile(self,user_id,data):
        print("inside create profile")
        # data = {}
        # if first_name: data["first_name"]=first_name
        # if last_name: data["last_name"]=last_name
        # if dob: data['dob']=dob
        # if phone: data["phone"]=phone
        # if residential_address: data["residential_address"]=residential_address
        # if id_image_url: data["id_image_url"]=id_image_url
        # if id_number: data["id_number"]=id_number
        # if gender: data["gender"]=gender


        allowed_keys = ["first_name","last_name","middle_name","dob","phone","gender","id_type","id_photo_url","id_number","residential_address"]
        ndata = {}
        for i in data.keys():
            if i in allowed_keys:
                ndata[i] = data[i]
        ndata["profile_completed"] = True
        user = db.users.update_one(
            {"_id": bson.ObjectId(user_id)},
            {
                "$set": ndata
            }
        )
        user = self.get_by_id(user_id)
        return user
    

    def get_all(self):
        """Get all users"""
        users = db.users.find({"active": True})
        return [{**user, "_id": str(user["_id"])} for user in users]

    def get_by_id(self, user_id):
        """Get a user by id"""
        user = db.users.find_one({"_id": bson.ObjectId(user_id), "active": True})
        if not user:
            return
        user["_id"] = str(user["_id"])
        user.pop("password")
        return user

    def get_by_email(self, email):
        """Get a user by email"""
        user = db.users.find_one({"email": email, "active": True})
        if not user:
            return
        user["_id"] = str(user["_id"])
        return user

    def update(self, user_id, data):
        """Update a user"""
        allowed_keys = ["first_name","last_name","middle_name","confirmed","confirmed_on","profile_completed","dob","phone","gender","id","id_photo_url","id_number","residential_address"]
        ndata = {}
        for i in data.keys():
            if i in allowed_keys:
                ndata[i] = data[i]

        user = db.users.update_one(
            {"_id": bson.ObjectId(user_id)},
            {
                "$set": ndata
            }
        )
        user = self.get_by_id(user_id)
        return user
    
    def delete(self, user_id):
        """Delete a user"""
        FarmProject().delete_by_user_id(user_id)
        user = db.users.delete_one({"_id": bson.ObjectId(user_id)})
        user = self.get_by_id(user_id)
        return user

    def disable_account(self, user_id):
        """Disable a user account"""
        user = db.users.update_one(
            {"_id": bson.ObjectId(user_id)},
            {"$set": {"active": False}}
        )
        user = self.get_by_id(user_id)
        return user

    def encrypt_password(self, password):
        """Encrypt password"""
        return generate_password_hash(password)

    def login(self, email, password):
        """Login a user"""
        user = self.get_by_email(email)
        if not user or not check_password_hash(user["password"], password):
            return
        user.pop("password")
        return user



class FarmerProfile():
    """Farmer Profile Model"""

    def __init__(self):
        return

    def create(self,user_id,highest_ed="",years_of_exp="",cv_file_url=""):
        """ Create Farmer Profile """
        new_farm_profile = db.farmer_profile.insert_one(
            {
                "user_id": user_id,
                "highest_ed": highest_ed,
                "years_of_exp": years_of_exp,
                "cv_file_url": cv_file_url
            }
        )
        return self.get_by_id(new_farm_profile.inserted_id)
    
    def get_by_id(self, profile_id):
        """ Get a profile by id """
        farmer = db.farmer_profile.find_one({"_id": bson.ObjectId(profile_id)})
        if not farmer:
            return
        farmer["_id"] = str(farmer["_id"])
        return farmer
    
    def get_all(self):
        """Get all farmer Profiles"""
        profiles = db.farmer_profile.find()
        return [{**profile, "_id": str(profile["_id"])} for profile in profiles]


class Sponserd():
    """Sponsord Farm model"""

    def __init__(self):
        return
    
    def create(self,user_id="",project_id="",harvest_type="",name="",unit_number="",note="",payment_type="",crop_type="",total_amount="",cost_per_unit="",ROS=""):
        print("about to create a sponser")
        print(harvest_type)
        if not project_id:
            return {
                "message":"project id is missing. You should provide one."
            }, 400
        sponsord_project = db.sponsord.insert_one(
            {
                "name": name,
                "user_id": user_id,
                "project_id": project_id,
                "harvest_type": harvest_type,
                "crop_type":crop_type,
                "units": unit_number,
                "note": note,
                "payment_type": payment_type,
                "total_amount": total_amount,
                "cost_per_unit": cost_per_unit,
                "ROS": ROS,
                "payed": False,
                "progress": [],
                "finance":""
            }

        )
        return self.get_by_id(sponsord_project.inserted_id)
    
    def update(self, spons_id, data):
        """Update a user"""
        allowed_keys = ["name","harvest_type","units","note","payment_type","total_amount"]
        ndata = {}
        for i in data.keys():
            if i in allowed_keys:
                ndata[i] = data[i]

        spons = db.sponsord.update_one(
            {"_id": bson.ObjectId(spons_id)},
            {
                "$set": ndata
            }
        )
        user = self.get_by_id(spons_id)
        return user
    
    def get_by_id(self, sponsord_id):
        """ Get a model by id """
        sponsord = db.sponsord.find_one({"_id": bson.ObjectId(sponsord_id)})
        if not sponsord:
            return {
                "message": "Sponsored Data not found",
                "data": None
            },404
        sponsord["_id"] = str(sponsord["_id"])
        return sponsord
    
    def pay(self, sponsord_id):
        sponss = db.sponsord.update_one(
            {"_id": bson.ObjectId(sponsord_id)},
            {"$set": {
                "payed": True,
                "payment_time": datetime.now(),
                "transaction_id":"rfdis45646sd"
            }}
        )
        spons = self.get_by_id(sponsord_id)
        spons["_id"] = str(spons.get("_id"))
        return spons

    
    def get_all(self):
        """Get all sponsord profile"""
        profiles = db.farmer_profile.find()
        return [{**profile, "_id": str(profile["_id"])} for profile in profiles]
    
    def get_by_user_id(self, user_id):
        """ Get a models by user_id """
        sponsord = db.sponsord.find({"user_id": user_id})
        return [{**sponsor, "_id": str(sponsor["_id"])} for sponsor in sponsord]
    
    # def get_by_user_id_and_sponsord_id(self, user_id, sponser):
    #     """Get a project given its title and author"""
    #     project = db.projects.find_one({"user_id": user_id, "title": title})
    #     if not project:
    #         return
    #     project["_id"] = str(project["_id"])
    #     return project