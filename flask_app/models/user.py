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
        return is_valid