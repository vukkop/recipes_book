from flask_app import app
from flask import render_template,redirect,request,session
from flask_app.models.model_user import User
from flask_app.models.model_ingredient import Ingredient
from flask_app.models.model_recipe import Recipe
import cloudinary

#create
@app.route("/recipe/new")
def new_recipe():
  if 'user_id' not in session:
    return redirect("/")
  if 'recipe_id' not in session:
    recipe = {
      "title": "",
      "description": "",
      "instructions": "",
      "category": "",
      "meal_of_day": "",
      "course": "",
      "cook_time": "",
      "servings": "",
    }
  else:
    recipe = Recipe.get_by_id(session['recipe_id'])

  user = User.get_by_id(session['user_id'])
  ingredients = Ingredient.get_all()
  return render_template("new_recipe.html",user=user, ingredients=ingredients, recipe=recipe)

# @app.route("/img/upload", methods = ["POST"])
# def upload_img():
#   file_to_upload = request.files['image']
#   app.logger.info('%s file_to_upload', file_to_upload)
#   Recipe.upload(file_to_upload)

@app.route("/recipe/create", methods = ["POST"])
def create_recipe():

  data = {
    **request.form,
    'user_id' : session['user_id'],
  }

  if 'is_favorite' not in data:
    data['is_favorite'] = 0
  # # if not Recipe.validate_create(data):
  # #   return redirect('/recipe/new')

  recipe_id = Recipe.save(data)
  session['recipe_id'] = recipe_id
  return redirect('/recipe/new')

@app.route("/add_ingredient", methods = ["POST"])
def add_ingredient():
  ing = Ingredient.get_by_id(request.form["id"])
  data = {
          "id": ing.id,
          "name": ing.name,
          "quantity": request.form["quantity"],
          "unit": request.form["unit"],
          "recipe_id" : session["recipe_id"]
          }
  Recipe.add_ingredient(data)

  return redirect("/recipe/new")



#read
@app.route("/recipe/show/<int:id>")
def display_recipe(id):
  if 'user_id' not in session:
    return redirect("/")
  user = User.get_by_id(session['user_id'])
  recipe = Recipe.get_one(id)
  return render_template("display_recipe.html", recipe=recipe, user=user)

#update
@app.route("/recipe/edit/<int:id>")
def edit_recipe(id):
  if 'user_id' not in session:
    return redirect("/")
  user = User.get_by_id(session['user_id'])
  recipe = Recipe.get_by_id(id)
  return render_template("edit_recipe.html", recipe=recipe, user=user)

@app.route("/recipe/<int:id>/update", methods = ["POST"])
def update_recipe(id):
  if 'user_id' not in session:
    return redirect("/")
  data = {
    **request.form,
    'id': id}
  # if not Recipe.validate_create(data):
  #   return redirect(f'/recipe/{id}/edit')
  Recipe.update(data)
  return redirect("/dashboard")

#delete
@app.route("/recipe/<int:id>/delete")
def delete_recipe(id):
  if 'user_id' not in session:
    return redirect("/")
  Recipe.delete(id)
  return redirect("/dashboard")

