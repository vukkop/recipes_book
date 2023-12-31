from flask_app import app
from flask_app.config.mysqlconnection import connectToMySQL
from flask_app import DB, bcrypt
from flask import flash, session

class Ingredient:

  def __init__( self , data ):
    self.id = data['id']
    self.name = data['name']
    self.created_at = data['created_at']
    self.updated_at = data['updated_at']


  @classmethod
  def save(cls, data):
    query = """INSERT INTO ingredients (name)
              VALUES ( %(name)s);"""
    return connectToMySQL(DB).query_db( query, data )

  @classmethod
  def get_all(cls):
    query = "SELECT * FROM ingredients"
    results = connectToMySQL(DB).query_db( query )
    return results

  @classmethod
  def delete(cls, id):
    query = "DELETE FROM ingredients WHERE id = %(id)s;"
    return connectToMySQL(DB).query_db(query, {'id':id})

  @classmethod
  def remove(cls, recipe_id, ingredient_id):
    query = "DELETE FROM recipes_has_ingredients WHERE (recipe_id = %(recipe_id)s) and (ingredient_id = %(ingredient_id)s);;"
    return connectToMySQL(DB).query_db(query, {'recipe_id': recipe_id,'ingredient_id': ingredient_id})

  @classmethod
  def get_by_id(cls, id):
    query = "SELECT * FROM ingredients WHERE id = %(id)s"
    results = connectToMySQL(DB).query_db(query, {'id': id})
    if results:
      dict = results[0]
      return cls(dict)


  @classmethod
  def update(cls, data):
    query = """UPDATE ingredients
      SET name = %(name)s
      WHERE id = %(id)s;"""
    return connectToMySQL(DB).query_db( query, data)

