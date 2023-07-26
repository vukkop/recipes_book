from flask_app import app
from flask_app.config.mysqlconnection import connectToMySQL
from flask_app import DB, bcrypt
from flask import flash, session
from flask import jsonify
import re, os, cloudinary
from flask_app.models import model_user, model_ingredient

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
PASSWORD_REGEX = re.compile(r'^(?=.*?[A-Z])(?=.*?[a-z])(?=.*?[0-9]).{8,}$')
''' (?=.*?[A-Z]) : At least one upper case English letter
    (?=.*?[a-z]) : At least one lower case English letter
    (?=.*?[0-9]) : At least one digit
    (?=.*?[#?!@$ %^&*-]) : At least one special character or space (not used in this case)
    .{8,} : Minimum eight in length
'''
NAME_REGEX = re.compile(r'^[a-zA-Z]+$')

class Recipe:

  def __init__( self , data ):
    self.id = data['id']
    self.title = data['title']
    self.description = data['description']
    self.instructions = data['instructions']
    self.cook_time = data['cook_time']
    self.servings = data['servings']
    self.meal_of_day = data['meal_of_day']
    self.category = data['category']
    self.course = data['course']
    self.is_favorite = data['is_favorite']
    self.image = data['image']
    self.created_at = data['created_at']
    self.updated_at = data['updated_at']

#create
  @classmethod
  def save(cls, data):
    query = """INSERT INTO recipes ( title, description, instructions, cook_time, servings, meal_of_day, category, course, is_favorite, image, user_id)
              VALUES ( %(title)s, %(description)s, %(instructions)s, %(cook_time)s, %(servings)s, %(meal_of_day)s, %(category)s, %(course)s, %(is_favorite)s, %(image)s, %(user_id)s);"""
    return connectToMySQL(DB).query_db( query, data )

  @classmethod
  def add_ingredient(cls, data):
    print(data)
    query = """INSERT INTO recipes_has_ingredients ( recipe_id, ingredient_id, unit, quantity)
              VALUES ( %(recipe_id)s, %(id)s, %(unit)s, %(quantity)s);"""
    return connectToMySQL(DB).query_db( query, data )

#read
  @classmethod
  def get_all(cls):
    query = "SELECT * FROM recipes JOIN users ON recipes.user_id = users.id;"
    results = connectToMySQL(DB).query_db( query )

    all_recipes = []

    for user_dict in results:
      recipe_instance = cls(user_dict)
      user_data = {
        'id' : user_dict['users.id'],
        'created_at' : user_dict['users.created_at'],
        'updated_at' : user_dict['users.updated_at'],
        'first_name' : user_dict['first_name'],
        'last_name' : user_dict['last_name'],
        'email' : user_dict['email'],
        'password' : user_dict['password'],
      }
      user_instance = model_user.User(user_data)
      recipe_instance.user = user_instance
      all_recipes.append(recipe_instance)
    return all_recipes


  @classmethod
  def get_recipe_ingredients(cls, id):
    query = "SELECT * FROM recipes_has_ingredients WHERE recipe_id = %(id)s"
    results = connectToMySQL(DB).query_db(query, {'id':id})
    i_list = []
    for one in results:
      ing = model_ingredient.Ingredient.get_by_id(one['ingredient_id'])
      ing.quantity = one["quantity"]
      ing.unit = one["unit"]
      i_list.append(ing)
    return i_list

  @classmethod
  def get_by_id(cls, id):
    query = "SELECT * FROM recipes WHERE id = %(id)s"
    results = connectToMySQL(DB).query_db(query, {'id': id})
    if results:
      dict = results[0]
      recipe = cls(dict)
      recipe.ingredients = cls.get_recipe_ingredients(id)
      return recipe

  @classmethod
  def get_one(cls, id):
    query = "SELECT * FROM recipes JOIN users ON recipes.user_id = users.id WHERE recipes.id = %(id)s;"
    results = connectToMySQL(DB).query_db(query, {'id': id})
    if results:
      user_dict = results[0]
      recipe_instance = cls(user_dict)
      user_data = {
        'id' : user_dict['users.id'],
        'created_at' : user_dict['users.created_at'],
        'updated_at' : user_dict['users.updated_at'],
        'first_name' : user_dict['first_name'],
        'last_name' : user_dict['last_name'],
        'email' : user_dict['email'],
        'password' : user_dict['password'],
      }
      user_instance = model_user.User(user_data)
      recipe_instance.user = user_instance
    return recipe_instance

#update
  @classmethod
  def update(cls, data):
    query = """UPDATE recipes
      SET title = %(title)s, description = %(description)s, instructions = %(instructions)s, cook_time = %(cook_time)s, servings = %(servings)s, meal_of_day = %(meal_of_day)s, category = %(category)s, course = %(course)s, is_favorite = %(is_favorite)s, image = %(image)s
      WHERE id = %(id)s;"""
    return connectToMySQL(DB).query_db( query, data)


  # @staticmethod
  # def upload(file):
  #   cloudinary.config(cloud_name = os.getenv('CLOUD_NAME'), api_key=os.getenv('API_KEY'),
  #   api_secret=os.getenv('API_SECRET'))

  #   if file:
  #     upload_result = cloudinary.uploader.upload(file)
  #     app.logger.info(upload_result)
  #     print(jsonify(upload_result))
  #     return jsonify(upload_result)

#delete
  @classmethod
  def delete(cls, id):
    query_c = "DELETE FROM recipes_has_ingredients WHERE recipe_id = %(id)s;"
    connectToMySQL(DB).query_db(query_c, {'id':id})
    query_p = "DELETE FROM recipes WHERE id = %(id)s;"
    return connectToMySQL(DB).query_db(query_p, {'id':id})

  @staticmethod
  def validate_create(data):
    is_valid = True

    if len(data['name']) < 1:
      flash("Please fill in name for the recipe", "err_name")
      is_valid = False

    if len(data['description']) < 1:
      flash("Please fill in description for the recipe.", "err_description")
      is_valid = False

    if len(data['instructions']) < 1:
      flash("Please fill in instructions for the recipe.", "err_instructions")
      is_valid = False

    if len(data['date_made']) < 1:
      flash("Please fill in date you made the dish.", "err_date_made")
      is_valid = False

    if 'under_30' not in data:
      flash("Please select one of the options.", "err_under_30")
      is_valid = False

    return is_valid
