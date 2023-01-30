from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash
from flask_app import DATABASE
from flask_app.models.user_model import User

class Car:
    def __init__(self, data):
        self.id = data['id']
        self.price = data['price']
        self.model = data['model']
        self.make = data['make']
        self.year = data['year']
        self.description = data['description']
        self.user_id = data['user_id']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']

    @classmethod
    def create(cls, data):
        query = '''
                INSERT INTO cars(price, model, make, year, description, user_id)
                VALUES (%(price)s, %(model)s, %(make)s, %(year)s, %(description)s, %(user_id)s);
                '''
        return  connectToMySQL(DATABASE).query_db(query, data)

    @classmethod
    def get_all_with_users( cls ):
        query = '''
                SELECT * FROM cars
                JOIN users ON cars.user_id = users.id;
                '''
        results = connectToMySQL(DATABASE).query_db(query)
        list_cars = []

        for row in results:
            current_car = cls( row )
            user_data = {
                **row,
                "created_at" : row['users.created_at'],
                "updated_at" : row['users.updated_at'],
                "id" : row['users.id']
            }
            current_user = User( user_data )
            current_car.user = current_user
            list_cars.append( current_car )
        return list_cars

    @classmethod
    def get_one_with_user( cls, data ):
        query = '''
                SELECT * FROM cars
                JOIN users ON cars.user_id = users.id
                WHERE cars.id = %(id)s;
                '''
        result = connectToMySQL(DATABASE).query_db(query, data)
        if result:
            current_car = cls( result[0])
            user_data = {
                **result[0],
                "created_at" : result[0]['users.created_at'],
                "updated_at" : result[0]['users.updated_at'],
                "id" : result[0]['users.id']
            }
            current_car.user = User( user_data ) 
            return current_car
        else: 
            return None

    @classmethod
    def update_one( cls, data ):
        query = '''
                UPDATE cars
                SET price = %(price)s, model = %(model)s, make = %(make)s, 
                year = %(year)s, description= %(description)s, user_id = %(user_id)s
                WHERE id = %(id)s;
                '''
        return connectToMySQL(DATABASE).query_db(query, data)

    @classmethod
    def delete_one(cls, data):
        query = '''
                DELETE FROM cars
                WHERE id = %(id)s;
                '''
        return connectToMySQL(DATABASE).query_db(query, data)

    @staticmethod
    def validate_car(data):
        is_valid = True
        if data['price'] == "":
            flash("Price is required and must not be left empty", "error_car_price")
            is_valid = False
        if data['model'] == "":
            flash("Model is required and must not be left empty", "error_car_model")
            is_valid = False
        if data['make'] == "":
            flash("Make is required and must not be left empty", "error_car_make")
            is_valid = False
        if data['year'] == "":
            flash("Year is required and must not be left empty", "error_car_year")
            is_valid = False
        if data['description'] == "":
            flash("Description is required and must not be left empty", "error_car_description")
            is_valid = False
        if len(data['year']) < 1:
            flash("Year must be greater than 0", "error_car_year")
            is_valid = False
        if len(data['price']) < 1:
            flash("Price must be greater than 0", "error_car_price")
            is_valid = False
        return is_valid

    
