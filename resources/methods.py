
    @classmethod
    def save(cls, data):
        query = """INSERT INTO users 
        (first_name, last_name, email, password, birthday, gender, language ,created_at, updated_at) 
        VALUES ( %(first_name)s , %(last_name)s , %(email)s , %(password)s, %(birthday)s, %(gender)s, %(language)s, NOW() , NOW() )
        ;"""
        result = connectToMySQL(cls.db).query_db( query, data )
        return result

    @classmethod
    def update(cls, data):
        query = """UPDATE users 
        SET first_name = %(first_name)s, last_name = %(last_name)s, email = %(email)s, updated_at = NOW() 
        WHERE id = %(id)s
        ;"""
        print(query)
        result = connectToMySQL(cls.db).query_db( query, data )
        print("||-- Items updated in database --|| <> Results:", result)
        return result

    @classmethod
    def delete(cls, data):
        query = """DELETE 
        FROM users 
        WHERE id = %(id)s
        ;"""
        result = connectToMySQL(cls.db).query_db( query, data )
        print("||-- Items deleted from database --|| <> Results:", result)
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
        FROM recipes 
        WHERE id = %(id)s
        ;"""
        result = connectToMySQL(cls.db).query_db(query,data)
        print("||-- Selected by id from database --|| <> Results:", result)
        if len(result) < 1:
            return False
        return cls(result[0])

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
        if len(data['birthday']) < 1:
            flash("Birthday is required.")
            is_valid = False
        if len(data['gender']) < 1:
            flash("Gender is required.")
            is_valid = False
        if len(data['language']) < 1:
            flash("Language is required.")
            is_valid = False
        if passwords['password'] != passwords['confirm_password']:
            flash("Passwords must be the same.")
            is_valid = False
        if len(passwords['password']) < 8:
            flash("Passwords must be longer than 8 characters.")
            is_valid = False
        return is_valid
