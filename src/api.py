import sqlite3
from flask import Flask, request, jsonify, abort
import string
import random
app = Flask(__name__)

# API Key for authentication

LENGTH = 4
api_key = ''.join(random.choices(string.ascii_uppercase + string.digits, k=LENGTH)+"-")

api_key = 'XTG34IU3P4O2TOHU245GHU245GPI45GPIHU45GPO425GPU45GPHU'

print("YOUR API KEY IS : \n", api_key)

# Authentication check
def check_api_key():
    api_key = request.headers.get('X-API-Key')
    if api_key != api_key:
        abort(401, description="Unauthorized. Invalid API key.")

# Connect to the database
def get_db_connection():
    conn = sqlite3.connect('/Users/aarush/Documents/Coding/TASK-FORCE-TRYOUTS-STARTER/src/recipes.db')
    conn.row_factory = sqlite3.Row  # This allows us to access columns by name
    return conn

# Input validation for integers (used for recipe ID)
def validate_id(value):
    try:
        value = int(value)
        return value
    except ValueError:
        abort(400, description="Invalid ID. Must be an integer.")

# Get all recipes
@app.route('/api/v1/recipes', methods=['GET'])
def get_recipes():
    check_api_key()
    conn = get_db_connection()
    recipes = conn.execute('SELECT * FROM recipes').fetchall()
    conn.close()

    return jsonify([dict(recipe) for recipe in recipes]), 200

# Get a recipe by ID
@app.route('/api/v1/recipes/<int:recipe_id>', methods=['GET'])
def get_recipe(recipe_id):
    check_api_key()
    recipe_id = validate_id(recipe_id)

    conn = get_db_connection()
    recipe = conn.execute('SELECT * FROM recipes WHERE id = ?', (recipe_id,)).fetchone()
    conn.close()

    if recipe is None:
        abort(404, description="Recipe not found.")
    
    return jsonify(dict(recipe)), 200

# Create a new recipe
@app.route('/api/v1/recipes', methods=['POST'])
def create_recipe():
    check_api_key()
    if not request.is_json:
        abort(400, description="Invalid data. JSON required.")
    
    data = request.get_json()
    title = data.get('title')
    ingredients = data.get('ingredients')
    instructions = data.get('instructions')

    if not title or not ingredients or not instructions:
        abort(400, description="Missing required fields.")

    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('''
        INSERT INTO recipes (title, ingredients, instructions) 
        VALUES (?, ?, ?)
    ''', (title, ingredients, instructions))
    conn.commit()
    recipe_id = cur.lastrowid
    conn.close()

    return jsonify({'id': recipe_id, 'title': title, 'ingredients': ingredients, 'instructions': instructions}), 201

# Update a recipe
@app.route('/api/v1/recipes/<int:recipe_id>', methods=['PUT'])
def update_recipe(recipe_id):
    check_api_key()
    recipe_id = validate_id(recipe_id)

    conn = get_db_connection()
    recipe = conn.execute('SELECT * FROM recipes WHERE id = ?', (recipe_id,)).fetchone()

    if recipe is None:
        conn.close()
        abort(404, description="Recipe not found.")
    
    if not request.is_json:
        conn.close()
        abort(400, description="Invalid data. JSON required.")

    data = request.get_json()
    title = data.get('title', recipe['title'])
    ingredients = data.get('ingredients', recipe['ingredients'])
    instructions = data.get('instructions', recipe['instructions'])

    conn.execute('''
        UPDATE recipes 
        SET title = ?, ingredients = ?, instructions = ? 
        WHERE id = ?
    ''', (title, ingredients, instructions, recipe_id))
    conn.commit()
    conn.close()

    return jsonify({'id': recipe_id, 'title': title, 'ingredients': ingredients, 'instructions': instructions}), 200

# Delete a recipe
@app.route('/api/v1/recipes/<int:recipe_id>', methods=['DELETE'])
def delete_recipe(recipe_id):
    check_api_key()
    recipe_id = validate_id(recipe_id)

    conn = get_db_connection()
    recipe = conn.execute('SELECT * FROM recipes WHERE id = ?', (recipe_id,)).fetchone()

    if recipe is None:
        conn.close()
        abort(404, description="Recipe not found.")

    conn.execute('DELETE FROM recipes WHERE id = ?', (recipe_id,))
    conn.commit()
    conn.close()

    return '', 204

if __name__ == '__main__':
    app.run(debug=True)
