from flask_app import app
from flask_app.config.mysqlconnection import connectToMySQL
from flask_app import DB, bcrypt
from flask import flash, session

class Shopping_List_Item:

  def __init__( self , data ):
    self.id = data['id']
    self.name = data['name']
    self.quantity = data['quantity']
    self.unit = data['unit']
    self.created_at = data['created_at']
    self.updated_at = data['updated_at']

