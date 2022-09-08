from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash 
import re
from pprint import pprint

# Validation schematics
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

class User:
    db = "private_wall"  # <--- Enter database reference
    def __init__(self ,data):
        self.id = data['id']
        self.first_name = data['first_name']
        self.last_name = data['last_name']
        self.email = data['email']
        self.password = data['password']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.associated = ""

# Utilize classmethod templates found in resources

    @classmethod
    def save(cls, data):
        query = """INSERT INTO users 
        (first_name, last_name, email, password, created_at, updated_at) 
        VALUES ( %(first_name)s , %(last_name)s , %(email)s , %(password)s, NOW() , NOW() )
        ;"""
        result = connectToMySQL(cls.db).query_db( query, data )
        return result

    @classmethod
    def get_all(cls):
        query = """SELECT * 
        FROM users
        ;"""
        results = connectToMySQL(cls.db).query_db(query)
        data = []
        for item in results:
            data.append( cls(item) )
        return data

    @classmethod
    def get_by_email(cls,data):
        query = """SELECT * 
        FROM users 
        WHERE email = %(email)s
        ;"""
        result = connectToMySQL(cls.db).query_db(query,data)
        print("||-- Selected by email from database --|| <> Results:", result)
        if len(result) < 1:
            return False
        return cls(result[0])
    
    @classmethod
    def get_by_id(cls,data):
        query = """SELECT * 
        FROM users 
        WHERE id = %(id)s
        ;"""
        result = connectToMySQL(cls.db).query_db(query,data)
        print("||-- Selected by id from database --|| <> Results:", result)
        if len(result) < 1:
            return False
        return cls(result[0])

    @classmethod
    def get_all_sent_messages_by_id(cls, data):
        query = """SELECT * 
        FROM messages
        Where user_id = %(id)s
        ;"""
        results = connectToMySQL(cls.db).query_db(query, data)
        data = []
        for item in results:
            data.append( item )
        return data

    @classmethod
    def send_message(cls,data):
        query = """INSERT INTO messages 
        (user_id, receiver_id, message, created_at, updated_at) 
        VALUES ( %(user_id)s, %(receiver_id)s, %(message)s, NOW() , NOW() )
        ;"""
        result = connectToMySQL(cls.db).query_db( query, data )
        print("The send message query result is:", result)
        return result

 # ||| Joined Tables 1:n ||| -> Users have many recipes, we want to gather all recipes and their associated user information. For each of the recipes, we are segregating the user information, generating a user object, and assigning that user to the recipe they made.
    @classmethod
    def get_all_joined(cls):
        query = """SELECT * 
        FROM recipes 
        JOIN users 
        ON recipes.user_id = users.id
        ;"""
        results = connectToMySQL(cls.db).query_db(query)
        print(results)
        recipe_objects = []
        for item in results:
            recipe_data = {
                'id': item["id"],
                'name': item["name"],
                'instructions': item["instructions"], 
                'description': item["description"],
                'date_cooked': item["date_cooked"],
                'under_30': item["under_30"],
                'created_at': item["created_at"],
                'updated_at': item["updated_at"]
            }
            user_data = {
                'id': item["users.id"],
                'first_name': item["first_name"],
                'last_name': item["last_name"],
                'password': item["password"],
                'email': item["email"],
                'created_at': item["users.created_at"],
                'updated_at': item["users.updated_at"]
            }
            recipe_object = Recipe(recipe_data)
            recipe_object.posted_by = user.User(user_data)
            recipe_objects.append( recipe_object )
            print("||-- Recipe objects generated --|| <> ", recipe_object)
        return recipe_objects

    @staticmethod
    def validate_user(data):
        is_valid = True
        if len(data['first_name']) < 2:
            flash("First name is required.")
            is_valid = False
        if len(data['last_name']) < 2:
            flash("Last name is required.")
            is_valid = False
        # Check database to see if email already exists.
        users = User.get_all()
        for user in users:
            if user.email == data['email']:
                flash("Email already exists.")
                is_valid = False
        if len(data['email']) < 1:
            flash("Email is required.")
            is_valid = False
        if data['password'] != data['confirm_password']:
            flash("Passwords must be the same.")
            is_valid = False
        if len(data['password']) < 8:
            flash("Passwords must be longer than 8 characters.")
            is_valid = False
        if len(data['message']) < 5:
            flash("Message must be at lease 5 characters long.")
            is_valid = False
        return is_valid

    @staticmethod
    def validate_message(data):
        is_valid = True
        if len(data['message']) < 5:
            flash("Message must be at least 5 characters long.")
            is_valid = False
        return is_valid