from flask_app import app
from flask_app.config.mysqlconnection import connectToMySQL
from flask_app import DB, bcrypt
from flask import flash, session
from flask_app.models import model_shopping_list_item, model_recipe

class Shopping_List:

  def __init__( self , data ):
    self.id = data['id']
    self.name = data['name']
    self.created_at = data['created_at']
    self.updated_at = data['updated_at']

  @classmethod
  def save(cls, recipe_id):
    shopping_list = Shopping_List.get_id(session['user_id'])
    shopping_list.ingredients = model_recipe.Recipe.get_recipe_ingredients(recipe_id)

    for ingredient in shopping_list.ingredients:
      query = """INSERT INTO shopping_list_items (shopping_list_id, ingredient_id, quantity, unit)
                VALUES ( %(shopping_list_id)s,  %(ingredient_id)s,  %(quantity)s,  %(unit)s)"""
      connectToMySQL(DB).query_db( query, {
        'shopping_list_id': shopping_list.id,
        'ingredient_id': ingredient.id,
        'quantity': ingredient.quantity,
        'unit': ingredient.unit,
                                                  } )

  @classmethod
  def get_id(cls, user_id):
    query = """SELECT * FROM shopping_lists
            WHERE shopping_lists.user_id = %(user_id)s;"""
    results = connectToMySQL(DB).query_db(query, {'user_id': user_id})
    if results:
      dict = results[0]
      shopping_list = cls(dict)
    return shopping_list

  @classmethod
  def get_by_user_id(cls, user_id):
    query = """SELECT * FROM shopping_lists
            JOIN shopping_list_items
            ON shopping_lists.id = shopping_list_items.shopping_list_id
            JOIN ingredients
            ON shopping_list_items.ingredient_id = ingredients.id
            WHERE shopping_lists.user_id = %(user_id)s;"""
    results = connectToMySQL(DB).query_db(query, {'user_id': user_id})

    all_items = []

    if results:
      for item_dict in results:
        shopping_list_instance = cls(item_dict)
        item_data = {
          'id' : item_dict['shopping_list_items.id'],
          'name' : item_dict['ingredients.name'],
          'quantity' : item_dict['quantity'],
          'unit' : item_dict['unit'],
          'created_at' : item_dict['ingredients.created_at'],
          'updated_at' : item_dict['ingredients.updated_at'],
        }
        item_instance = model_shopping_list_item.Shopping_List_Item(item_data)
        all_items.append(item_instance)
        shopping_list_instance.items = all_items

      return shopping_list_instance

  # @classmethod
  # def remove(cls, recipe_id, ingredient_id):
  #   query = "DELETE FROM recipes_has_ingredients WHERE (recipe_id = %(recipe_id)s) and (ingredient_id = %(ingredient_id)s);;"
  #   return connectToMySQL(DB).query_db(query, {'recipe_id': recipe_id,'ingredient_id': ingredient_id})



  # @classmethod
  # def update(cls, data):
  #   query = """UPDATE ingredients
  #     SET name = %(name)s
  #     WHERE id = %(id)s;"""
  #   return connectToMySQL(DB).query_db( query, data)


  # @staticmethod
  # def validate_create(data):
  #   is_valid = True

  #   if len(data['name']) < 1:
  #     flash("Please fill in name for the recipe", "err_name")
  #     is_valid = False

  #   if len(data['description']) < 1:
  #     flash("Please fill in description for the recipe.", "err_description")
  #     is_valid = False

  #   if len(data['instructions']) < 1:
  #     flash("Please fill in instructions for the recipe.", "err_instructions")
  #     is_valid = False

  #   if len(data['date_made']) < 1:
  #     flash("Please fill in date you made the dish.", "err_date_made")
  #     is_valid = False

  #   if 'under_30' not in data:
  #     flash("Please select one of the options.", "err_under_30")
  #     is_valid = False

  #   return is_valid
