import unittest
import requests
import random
import sqlite3 as sql


BASE_URL = 'http://127.0.0.1:5000/api/v1/recipes'
API_KEY = 'XTG34IU3P4O2TOHU245GHU245GPI45GPIHU45GPO425GPU45GPHU'

# Common headers with API Key for authentication
HEADERS = {
    'X-API-Key': API_KEY,
    'Content-Type': 'application/json'
}

def get_db_connection():
    conn = sql.connect('/Users/aarush/Documents/Coding/TASK-FORCE-TRYOUTS-STARTER/src/recipes.db')
    conn.row_factory = sql.Row 
    return conn

def create_recipe():
    data = {
            'title': 'Spaghetti Bolognese',
            'ingredients': 'Spaghetti, minced beef, tomato sauce, onions, garlic, olive oil',
            'instructions': '1. Cook spaghetti. 2. Make sauce. 3. Mix and serve.'
        }
    
    title = data['title']
    ingredients = data['ingredients']
    instructions = data['instructions']

    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('''
        INSERT INTO recipes (title, ingredients, instructions) 
        VALUES (?, ?, ?)
    ''', (title, ingredients, instructions))
    
    conn.commit()
    return cur.lastrowid
    conn.close()

class TestRecipeAPI(unittest.TestCase):

    def setUp(self):
        self.recipe_id = None

    def test_1_create_recipe(self):
        
        """Test creating a new recipe"""

        new_recipe = {
            'title': 'Spaghetti Bolognese',
            'ingredients': 'Spaghetti, minced beef, tomato sauce, onions, garlic, olive oil',
            'instructions': '1. Cook spaghetti. 2. Make sauce. 3. Mix and serve.'
        }

        # Send POST request to create a new recipe
        response = requests.post(BASE_URL, headers=HEADERS, json=new_recipe)

        # Check if the request was successful (status code 201)
        self.assertEqual(response.status_code, 201, f"Failed to create recipe. Status code: {response.status_code}\n")

        # Store the created recipe's ID for other tests
        created_recipe = response.json()
        self.recipe_id = created_recipe['id']
        print(f"Created recipe: {created_recipe}\n")

    def test_2_get_recipe(self):
        """Test retrieving the created recipe"""
        self.recipe_id = create_recipe()
        # Ensure that recipe ID is set
        self.assertIsNotNone(self.recipe_id, "Recipe ID not set. Run create_recipe test first.\n")

        # Send GET request to retrieve the recipe by its ID
        response = requests.get(f'{BASE_URL}/{self.recipe_id}', headers=HEADERS)

        # Check if the request was successful (status code 200)
        self.assertEqual(response.status_code, 200, f"Failed to get recipe. Status code: {response.status_code}\n")

        # Get the response data and print
        recipe = response.json()
        print(f"Retrieved recipe: {recipe}\n")

    def test_3_update_recipe(self):
        """Test updating the created recipe"""
        # Ensure that recipe ID is set
        self.assertIsNotNone(self.recipe_id, "Recipe ID not set. Run create_recipe test first.\n")

        # Updated recipe data
        updated_recipe = {
            'title': 'Updated Spaghetti Bolognese',
            'ingredients': 'Nigattoni, minced beef, tomato sauce, onions, garlic, olive oil, basil',
            'instructions': '1. Cook spaghetti. 2. Make sauce with basil. 3. Mix and serve.'
        }

        # Send PUT request to update the recipe
        response = requests.put(f'{BASE_URL}/{self.recipe_id}', headers=HEADERS, json=updated_recipe)

        # Check if the request was successful (status code 200)
        self.assertEqual(response.status_code, 200, f"Failed to update recipe. Status code: {response.status_code}\n")

        # Get the response data and print
        updated_recipe_data = response.json()
        print(f"Updated recipe: {updated_recipe_data}")

    def test_4_delete_recipe(self):
        """Test deleting the created recipe"""
        # Ensure that recipe ID is set
        self.assertIsNotNone(self.recipe_id, "Recipe ID not set. Run create_recipe test first.\n")

        # Send DELETE request to delete the recipe by its ID
        response = requests.delete(f'{BASE_URL}/{self.recipe_id}', headers=HEADERS)

        # Check if the request was successful (status code 204)
        self.assertEqual(response.status_code, 204, f"Failed to delete recipe. Status code: {response.status_code}")

        print(f"Deleted recipe with ID: {self.recipe_id}")

    def test_5_get_deleted_recipe(self):
        """Test retrieving a deleted recipe (should return 404)"""
        # Ensure that recipe ID is set
        self.assertIsNotNone(self.recipe_id, "Recipe ID not set. Run create_recipe test first.\n")

        # Send GET request to retrieve the deleted recipe by its ID
        response = requests.get(f'{BASE_URL}/{self.recipe_id}', headers=HEADERS)

        # Check if the request returns 404 (Not Found)
        self.assertEqual(response.status_code, 404, f"Expected 404 for deleted recipe, but got {response.status_code}\n")


if __name__ == '__main__':
    # Run the unittests
    unittest.main()
