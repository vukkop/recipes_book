from flask_app.config.mysqlconnection import connectToMySQL
from flask_app import DB
from flask import flash
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

class Sighting:

  def __init__( self , data ):
    self.id = data['id']
    self.location = data['location']
    self.what_happened = data['what_happened']
    self.date_of_sighting = data['date_of_sighting']
    self.num_of_sasquatches = data['num_of_sasquatches']
    self.created_at = data['created_at']
    self.updated_at = data['updated_at']



  #create
  @classmethod
  def save(cls, data):
    query = "INSERT INTO sightings ( location, what_happened, date_of_sighting, num_of_sasquatches, user_id) VALUES ( %(location)s, %(what_happened)s, %(date_of_sighting)s, %(num_of_sasquatches)s, %(user_id)s);"
    return connectToMySQL(DB).query_db( query, data )

  @classmethod
  def get_all(cls):
    query = "SELECT * FROM sightings JOIN users ON sightings.user_id = users.id;"
    results = connectToMySQL(DB).query_db( query )

    all_sightings = []

    for user_dict in results:
      sighting_instance = cls(user_dict)
      user_data = {
        **user_dict,
        'id' : user_dict['users.id'],
        'first_name' : user_dict['first_name'],
        'last_name' : user_dict['last_name'],
        'email' : user_dict['email'],
        'password' : user_dict['password'],
      }
      user_instance = model_user.User(user_data)
      sighting_instance.user = user_instance
      all_sightings.append(sighting_instance)
    return all_sightings

  @classmethod
  def get_by_id(cls, id):
    query = "SELECT * FROM sightings WHERE id = %(id)s"
    results = connectToMySQL(DB).query_db(query, {'id': id})
    if results:
      dict = results[0]
      return cls(dict)

  @classmethod
  def get_one(cls, id):
    query = "SELECT * FROM sightings JOIN users ON sightings.user_id = users.id WHERE sightings.id = %(id)s;"
    results = connectToMySQL(DB).query_db(query, {'id': id})
    if results:
      user_dict = results[0]
      sighting_instance = cls(user_dict)
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
      sighting_instance.user = user_instance
    return sighting_instance


  @classmethod
  def update(cls, data):
    query = "UPDATE sightings SET location = %(location)s, what_happened = %(what_happened)s, date_of_sighting = %(date_of_sighting)s, num_of_sasquatches = %(num_of_sasquatches)s WHERE id = %(id)s;"
    return connectToMySQL(DB).query_db( query, data)

  @classmethod
  def delete(cls, id):
    query = "DELETE FROM sightings WHERE id = %(id)s;"
    return connectToMySQL(DB).query_db(query, {'id':id})

  @staticmethod
  def validate_create(data):
    is_valid = True

    if len(data['location']) < 1:
      flash("Please fill in location of the sighting.", "err_location")
      is_valid = False

    if len(data['what_happened']) < 1:
      flash("Please fill in what happened on the sighting.", "err_what_happened")
      is_valid = False

    if len(data['date_of_sighting']) < 1:
      flash("Please fill in date of the sighting.", "err_date_of_sighting")
      is_valid = False

    if len(data['num_of_sasquatches']) < 1 or int(data['num_of_sasquatches']) < 1:
      flash("Please fill in number valid of sasquatches on the sighting.", "err_num_of_sasquatches")
      is_valid = False

    return is_valid
