"""Validator Module"""
import re
from bson.objectid import ObjectId

def validate(data, regex):
    """Custom Validator"""
    return True if re.match(regex, data) else False

def validate_password(password: str):
    """Password Validator"""
    reg = r"\b^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*#?&])[A-Za-z\d@$!#%*?&]{8,20}$\b"
    return validate(password, reg)

def validate_email(email: str):
    """Email Validator"""
    regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
    return validate(email, regex)

def validate_date(date: str):
    """Date Validator"""
    regex = r'^\d{4}\-(0?[1-9]|1[012])\-(0?[1-9]|[12][0-9]|3[01])$'
    return validate(date, regex)

def validate_project(**args):
    """Add available resources array funds, equipment, land"""
    """project Validator"""
    if not args.get('title') or not args.get('image_url') or not args.get('description') \
        or not args.get('product') or not args.get('resources'):
        return {
            'title': 'Title is required',
            'image_url': 'Image URL is required',
            'product': 'product is required',
            'description': 'Description is required',
            'resources': "Resources required"
        }
    try:
        ObjectId(args.get('user_id'))
    except Exception as e:
        print(e)
        return {
            'user_id': 'User ID must be valid'
        }
    if not isinstance(args.get('title'), str) or not isinstance(args.get('product'), str) or not isinstance(args.get('description'), str) \
        or not isinstance(args.get('image_url'), str):
        return {
            'title': 'Title must be a string',
            'description': 'Description must be a string',
            'product': 'Product must be a string',
            'image_url': 'Image URL must be a string',
        }
    return True

def validate_user(**args):
    """User Validator"""
    if  not args.get('email') or not args.get('password') or not args.get('name'):
        return {
            'email': 'Email is required',
            'password': 'Password is required',
            'name': 'Name is required'
        }
    if not isinstance(args.get('name'), str) or \
        not isinstance(args.get('email'), str) or not isinstance(args.get('password'), str):
        return {
            'email': 'Email must be a string',
            'password': 'Password must be a string',
            'name': 'Name must be a string'
        }
    if not validate_email(args.get('email')):
        return {
            'email': 'Email is invalid'
        }
    if not validate_password(args.get('password')):
        return {
            'password': 'Password is invalid, Should be atleast 8 characters with \
                upper and lower case letters, numbers and special characters'
        }
    if not 2 <= len(args['name'].split(' ')) <= 30:
        return {
            'name': 'Name must be between 2 and 30 words'
        }
    return True

def validate_user_profile(**args):
    """Profile Validator"""
    if  not args.get('first_name') or not args.get('last_name') or not args.get('gender') or  not args.get('id_type') or\
        not args.get('dob') or not args.get('phone') or not args.get('id_number') or not args.get('residential_address'):
        return {
            'first_name': 'First Name is required',
            'last_name': 'Last Name is required',
            'dob': 'Date of birth is required',
            'phone': 'Phone is required',
            'residential_address': 'Residential Addrees is required',
            'id_number': 'ID card number is required',
            'gender':"gender is required"
        }
    if not isinstance(args.get('first_name'), str) or not isinstance(args.get('last_name'), str)  or\
        not isinstance(args.get('dob'), str) or not isinstance(args.get('phone'), str) or not isinstance(args.get('gender'),str) or\
        not isinstance(args.get('id_number'), str) or not isinstance(args.get('residential_address'), str) or not isinstance(args.get('id_image_url'), str):
        return {
            'first_name': 'First Name must be a string',
            'last_name': 'Last Name must be a string',
            'dob': 'Date of birth must be a string',
            'phone': 'Phone must be a string',
            'residential_address': 'Residential Address must be a string',
            'id_number': 'ID card number must be a string',
            "gender":"gender must be a string"
        }
    # if not validate_date(args.get('dob')):
    #     return {
    #         'DOB': 'Date of Birth is invalid'
    #     }
    
    if not (2 <= len(args['first_name'].split(' ')) <= 30) or (2 <= len(args['last_name'].split(' ')) <= 30):
        return {
            'name': 'Name must be between 2 and 30 words'
        }
    return True

def validate_email_and_password(email, password):
    """Email and Password Validator"""
    if not (email and password):
        return {
            'email': 'Email is required',
            'password': 'Password is required'
        }
    if not validate_email(email):
        return {
            'email': 'Email is invalid'
        }
    if not validate_password(password):
        return {
            'password': 'Password is invalid, Should be atleast 8 characters with \
                upper and lower case letters, numbers and special characters'
        }
    return True
