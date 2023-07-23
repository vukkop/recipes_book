from flask_app.config.mysqlconnection import connectToMySQL
from flask_app import DB, bcrypt
from flask import flash, session
import re
from flask_app.models import model_user

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
    self.name = data['name']
    self.description = data['description']
    self.instructions = data['instructions']
    self.date_made = data['date_made']
    self.under_30 = data['under_30']
    self.created_at = data['created_at']
    self.updated_at = data['updated_at']

  @classmethod
  def save(cls, data):
    query = "INSERT INTO recipes ( name, description, instructions, date_made, under_30, user_id) VALUES ( %(name)s, %(description)s, %(instructions)s, %(date_made)s, %(under_30)s, %(user_id)s);"
    return connectToMySQL(DB).query_db( query, data )

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
  def delete(cls, id):
    query = "DELETE FROM recipes WHERE id = %(id)s;"
    return connectToMySQL(DB).query_db(query, {'id':id})

  @classmethod
  def get_by_id(cls, id):
    query = "SELECT * FROM recipes WHERE id = %(id)s"
    results = connectToMySQL(DB).query_db(query, {'id': id})
    if results:
      dict = results[0]
      return cls(dict)

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


  @classmethod
  def update(cls, data):
    query = "UPDATE recipes SET name = %(name)s, description = %(description)s, instructions = %(instructions)s, date_made = %(date_made)s, under_30 = %(under_30)s WHERE id = %(id)s;"
    return connectToMySQL(DB).query_db( query, data)

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
