from flask_app.config.mysqlconnection import connectToMySQL
from flask_app.models import user
from flask import flash 
import re
from pprint import pprint

# Validation schematics
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

class Message:
    db = "private_wall"  # <--- Enter database reference
    def __init__(self ,data):
        self.id = data['id']
        self.user_id = data['user_id']
        self.receiver_id = data['receiver_id']
        self.message = data['message']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.sender = None
        self.time_difference = None

# Utilize classmethod templates found in resources

    @classmethod
    def get_messages_by_receiver_id(cls,data):
        query = """SELECT * 
        FROM users
        JOIN messages
        ON messages.receiver_id = users.id
        WHERE users.id = %(receiver_id)s
        ;"""
        results = connectToMySQL(cls.db).query_db(query,data)
        messages = []
        for item in results:
            message_data = {
                'id': item['messages.id'],
                'user_id': item['user_id'],
                'receiver_id':item['receiver_id'],
                'message': item['message'],
                'created_at': item['messages.created_at'],
                'updated_at': item['messages.updated_at']
            }
            user_data = {
                'id': item['user_id']
            }
            message_instance = cls(message_data)
            message_instance.sender = user.User.get_by_id(user_data)
            print("Message sender is:", message_instance.sender)
            messages.append( message_instance )
        print(messages)
        return messages

    @classmethod
    def delete_message(cls, data):
        query = """DELETE 
        FROM messages 
        WHERE id = %(id)s
        ;"""
        result = connectToMySQL(cls.db).query_db( query, data )
        return result

    @classmethod
    def send_message(cls,data):
        query = """INSERT INTO messages 
        (user_id, receiver_id, message, created_at, updated_at) 
        VALUES ( %(user_id)s, %(receiver_id)s, %(message)s, NOW() , NOW() )
        ;"""
        result = connectToMySQL(cls.db).query_db( query, data )
        print("The send message query result is:", result)
        return result