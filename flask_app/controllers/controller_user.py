from flask_app import app, bcrypt
from flask import render_template,redirect,request,session
from flask_app.models.model_user import User
from flask_app.models.model_recipe import Recipe
from flask_app.models.model_shopping_list import Shopping_List

#create
@app.route("/users/create", methods = ["POST"])
def create():
  data = {
    **request.form
  }

  if not User.validate_registration(data):
    return redirect('/')

  hash_pw = bcrypt.generate_password_hash(data['password'])
  data['password'] = hash_pw
  user_id = User.save(data)
  session['user_id'] = user_id
  Shopping_List.save(user_id)
  return redirect("/dashboard")

#read
@app.route("/dashboard")
def home():
  if 'user_id' not in session:
    return redirect("/")
  if "recipe_id" in session:
    session.pop("recipe_id")
  user = User.get_by_id(session['user_id'])
  recipes = Recipe.get_all()
  return render_template("dashboard.html", user=user, recipes=recipes )

@app.route("/logout")
def logout():
  if 'user_id' in session:
    session.clear()
  return redirect("/")

@app.route("/login", methods = ["POST"])
def login():
  data = {
  **request.form
  }
  if not User.validate_login(data):
    return redirect("/")

  return redirect("/dashboard")
