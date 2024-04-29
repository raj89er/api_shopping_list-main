
from flask import request
from datetime import datetime, timezone
from app import app
from shopping_list import shopping_list
from .models import User, Ingredient
from auth import token_auth, basic_auth


users_list = []


@app.route('/', methods=['GET'])
def index():
    return '''
Hello There! ~General K.~ 
Welcome to the Shopping List API!
'''

# User Endpoints
# [POST] /users - Create a new user
@app.route('/users', methods=['POST'])
def create_user():
    # Error handling
    if not request.is_json:
        return {'error': 'Your content type must be in json'}, 400
    data = request.json
    missing_fields = []
    for field in ['firstName' , 'lastName' , 'username' , 'email' , 'password']:
        if field not in data:
            missing_fields.append(field)
    if missing_fields:
        return {'error': f'You are missing the following required fields: {", ".join(missing_fields)}'}, 400
    # Check if username or email already exists
    for user in users_list:
        if user['email'] == data['email'] or user['username'] == data['username']:
            return {'error': 'User with that username and/or email already exists'}, 409
    # Create a new user with the data received
    new_user = {
        'user_id': len(users_list) + 1,
        'username': data.get('username'),
        'name_first': data.get('description'),
        'name_last': data.get('lastName'),
        'email': data.get('email'),
        'password': data.get('password'),
        'date_joined': datetime.now(timezone.utc).strftime('%Y-%m-%d')
        }
    # Add the new user to the users_list
    users_list.append(new_user)
    # Return a success message
    return new_user, 201

# [GET] /users/<user_id>
@app.route('/users/<int:user_id>', methods=['GET'])
def get_user(user_id):
    for user in users_list:
        if user['user_id'] == user_id:
            return {'user': user}
        else:
            return {'error': f'User with that ID does not exist'}, 404

# [PUT] /users/<user_id> *token auth required
@token_auth.login_required
@app.route('/users/<int:user_id>', methods=['PUT'])
def update_user(user_id):
    if not request.is_json:
        return {'error': 'Your content type must be in json'}, 400
    data = request.json
    current_user = token_auth.current_user()
    if current_user['user_id'] != user_id:
        return {'error': 'You are not authorized to update this user'}, 403
    for user in users_list:
        if user['user_id'] == user_id:
            user.update(data)
            return {'message': ' User <user_id> was updated successfully'}

# [DELETE] /users/<user_id>[DELETE] /users/<user_id>
@token_auth.login_required
@app.route('/users/<int:user_id>', methods=['DELETE'])
def delete_user(current_user, user_id):
    if current_user['user_id'] != user_id:
        return {'error': 'You are not authorized to delete this user'}, 403
    for user in users_list:
        if user['user_id'] == user_id:
            users_list.remove(user)
            return {'message': f'User {user_id} was deleted successfully'}
    return {'error': f'User with ID "{user_id}" does not exist'}, 404
    


# Ingredients Endpoints
# [GET] /tasks - Get all tasks 
@app.route('/ingredients', methods=['GET'])
def get_ingredients():
    return {'ingredients': shopping_list}

# [GET] /tasks/<task_id> - Get a task
@app.route('/ingredients/<int:ingredient_id>', methods=['GET'])
def get_ingredient(ingredient_id):
    for ingredient in shopping_list:
        if ingredient['ingredient_id'] == ingredient_id:
            return ingredient
    return {'error': f'ingredient with ID "{ingredient_id}" does not exist'}, 404

#[POST] /tasks/<task_id> - Get a task
@app.route('/ingredients', methods=['POST'])
def create_ingredient():
    # Error handling
    if not request.is_json:
        return {'error': 'Your content type must be in json'}, 400
    # Check for missing required fields (ingredient and description)
    data = request.json
    missing_fields = []
    for field in ['ingredient', 'description']:
        if field not in data:
            missing_fields.append(field)
    if missing_fields:
        return {'error': f'You are missing the following required fields: {", ".join(missing_fields)}'}, 400
    # Check if ingredient already exists
    for ingredient in shopping_list:
        if ingredient['ingredient'].lower() == data['ingredient'].lower():
            return {'error': 'Ingredient with that name already exists'}, 409
    # Create a new ingredient with the data received after error checking
    new_ingredient = {
        'ingredient_id': len(shopping_list) + 1,
        'ingredient': data['ingredient'],
        'description': data['description'],
        'status': False,
        'date_added': datetime.now(timezone.utc).strftime('%Y-%m-%d')
        }
    # Add the new ingredient to the shopping_list
    shopping_list.append(new_ingredient)
    # Return a success message and the updated shopping_list
    return new_ingredient, 201

# [PUT] /tasks/<task_id> *token auth required
@token_auth.login_required
@app.route('/ingredients/<int:ingredient_id>', methods=['PUT'])
def update_ingedient(ingredient_id):
    if not request.is_json:
        return {'error': 'Your content type must be in json'}, 400
    current_user = token_auth.current_user()
    if current_user['user_id'] != User.user_id:
        return {'error': 'You are not authorized to update this ingredient'}, 403
    data = request.json
    for ingredient in shopping_list:
        if ingredient['ingredient_id'] == ingredient_id:
            ingredient.update(data)
            return {'message': f'Ingredient {ingredient_id} was updated successfully'}
    return {'error': f'Ingredient with ID "{ingredient_id}" does not exist'}, 404

# [DELETE] /tasks/<task_id> *token auth required
@token_auth.login_required
@app.route('/ingredients/<int:ingredient_id>', methods=['DELETE'])
def delete_ingredient(ingredient_id):
    current_user = token_auth.current_user()
    if current_user['user_id'] != User.user_id:
        return {'error': 'You are not authorized to delete this ingredient'}, 403
    for ingredient in shopping_list:
        if ingredient['ingredient_id'] == ingredient_id:
            shopping_list.remove(ingredient)
            return {'message': f'Ingredient {ingredient_id} was deleted successfully'}
    return {'error': f'Ingredient with ID "{ingredient_id}" does not exist'}, 404
