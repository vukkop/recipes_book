from flask_app.config.mysqlconnection import connectToMySQL
from flask_app import DB, bcrypt
from flask import flash, session
import re

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
PASSWORD_REGEX = re.compile(r'^(?=.*?[A-Z])(?=.*?[a-z])(?=.*?[0-9]).{8,}$')
''' (?=.*?[A-Z]) : At least one upper case English letter
    (?=.*?[a-z]) : At least one lower case English letter
    (?=.*?[0-9]) : At least one digit
    (?=.*?[#?!@$ %^&*-]) : At least one special character or space (not used in this case)
    .{8,} : Minimum eight in length
'''
NAME_REGEX = re.compile(r'^[a-zA-Z]+$')

class User:

  def __init__( self , data ):
    self.id = data['id']
    self.first_name = data['first_name']
    self.last_name = data['last_name']
    self.email = data['email']
    self.password = data['password']
    self.created_at = data['created_at']
    self.updated_at = data['updated_at']

  #create
  @classmethod
  def save(cls, data):
    query = "INSERT INTO users ( first_name, last_name, email, password ) VALUES ( %(first_name)s, %(last_name)s, %(email)s, %(password)s );"
    return connectToMySQL(DB).query_db( query, data )

  #read
  @classmethod
  def get_by_email(cls, data):
    query = "SELECT * FROM users WHERE users.email = %(email)s"
    results = connectToMySQL(DB).query_db( query, data )
    if results:
      dict = results[0]
      return cls(dict)
    else:
      return None

  @classmethod
  def get_by_id(cls, id):
    query = "SELECT * FROM users WHERE users.id = %(id)s"
    results = connectToMySQL(DB).query_db(query, {'id': id})
    if results:
      dict = results[0]
      return cls(dict)

  #validate
  @staticmethod
  def validate_registration(data):
    is_valid = True

    if len(data['first_name']) < 3:
      flash("Please fill in your first name", "err_first_name")
      is_valid = False
    elif not NAME_REGEX.match(data['first_name']):
      flash("First name must contain only alphabetic characters.", "err_first_name")
      is_valid = False

    if len(data['last_name']) < 3:
      flash("Please fill in your last name.", "err_last_name")
      is_valid = False
    elif not NAME_REGEX.match(data['last_name']):
      flash("Last name must contain only alphabetic characters", "err_first_name")
      is_valid = False

    if len(data['email']) < 1:
      flash("Please fill in your email.", "err_email")
      is_valid = False
    elif not EMAIL_REGEX.match(data['email']):
      flash("Invalid email address.", "err_email")
      is_valid = False
    elif User.get_by_email(data):
      flash("Account with this email already exists.", "err_email")
      is_valid = False

    if not PASSWORD_REGEX.match(data['password']):
      flash("Password must contain at least 8 characters and 1 number, 1 lower case and 1 uppercase letter.", "err_password")
      is_valid = False

    if len(data['confirm_password']) < 8:
      flash("Please confirm your password.", "err_confirm_password")
      is_valid = False
    elif not data['password'] == data['confirm_password']:
      flash("Please confirm your password.", "err_confirm_password")
      is_valid = False

    return is_valid

  @staticmethod
  def validate_login(data):
    is_valid = True

    if len(data['email']) < 1:
      flash("Invalid username or password.", "err_login")
      is_valid = False
      return is_valid
    elif not EMAIL_REGEX.match(data['email']):
      flash("Invalid username or password.", "err_login")
      is_valid = False
      return is_valid

    if len(data['password']) < 9:
      flash("Invalid username or password.", "err_login")
      is_valid = False
      return is_valid

    if 'email' in data:
      potential_user = User.get_by_email(data)
      if not potential_user:
        flash("Invalid username or password.", "err_login")
        is_valid = False
        return is_valid

    if potential_user.password:
      if not bcrypt.check_password_hash(potential_user.password ,data['password']):
        flash("Invalid username or password.", "err_login")
        is_valid = False
        return is_valid

    session['user_id'] = potential_user.id
    return is_valid
