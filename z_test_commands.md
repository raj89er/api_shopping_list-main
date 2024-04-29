
# Next Step, add test ingredients to database

flask shell
NOT WORKING
new_ingredient1 = Ingredient(ingredient='Tomato', description='Fresh and juicy red tomatoes', status=False)
new_ingredient2 = Ingredient(ingredient='Onion', description='Crunchy and flavorful onions', status=True)
new_ingredient3 = Ingredient(ingredient='Lettuce', description='Crisp and leafy lettuce', status=False)

postman
WORKING
{ "ingredient": "onion", "description": "Make 'em cry" }
{ "ingredient": "tomato", "description": "veg, fruit, or berry?" }
{ "ingredient": "lettuce", "description": "...why though...?" }

Routes:
<!-- - [GET] /tasks - Get all tasks from the task table in a list of dictionaries -->
<!-- - [GET] /tasks/<task_id> - Get a task in dictionary form based on the ID or return a 404 status -->
<!-- - [POST] /tasks *token auth required - Create a new task with a title and description, returns the new task with a 201 status -->
<!-- - [PUT] /tasks/<task_id> *token auth required - Update a task by id, task must be created by user trying to update -->
- [DELETE] /tasks/<task_id> *token auth required - Delete a task by id, task must be created by user trying to delete

<!-- - [POST] /users - Create a new user with a username, email, and password with  -->
<!-- - [GET] /users/<user_id> - Get a user by id in dictionary form or return a 404 status -->
<!-- - [PUT] /users/<user_id> *token auth required - Update a user by id, user must be trying to update itself -->
<!-- - [DELETE] /users/<user_id> *token auth required - Delete a user by id, user must be trying to delete itself -->

<!-- - [GET] /token *basic auth required - returns a token based on username and password -->