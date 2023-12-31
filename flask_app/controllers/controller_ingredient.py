from flask_app import app
from flask import render_template,redirect,request,session
from flask_app.models.model_ingredient import Ingredient
from flask_app.models.model_user import User


#create
@app.route("/ingredient/create", methods = ["POST"])
def create_ingredient():
  data = {
    **request.form,
    'user_id' : session['user_id']
  }
  # if not Ingredient.validate_create(data):
  #   return redirect('/ingredient/new')

  Ingredient.save(data)
  return redirect('/ingredients')

#read
@app.route("/ingredients")
def ingredients():
  if 'user_id' not in session:
    return redirect("/")
  user = User.get_by_id(session['user_id'])
  ingredients = Ingredient.get_all()
  return render_template("ingredients.html", user=user, ingredients=ingredients )








#delete
@app.route("/ingredient/<int:id>/delete")
def delete_ingredient(id):
  if 'user_id' not in session:
    return redirect("/")
  Ingredient.delete(id)
  return redirect("/ingredients")

@app.route("/recipe/edit/<int:recipe_id>/ingredient/<int:ingredient_id>/remove")
def remove_ingredient_edit(recipe_id, ingredient_id):
  if 'user_id' not in session:
    return redirect("/")
  Ingredient.remove(recipe_id, ingredient_id)
  return redirect(f"/recipe/edit/{recipe_id}")

@app.route("/recipe/new/<int:recipe_id>/ingredient/<int:ingredient_id>/remove")
def remove_ingredient_new(recipe_id, ingredient_id):
  if 'user_id' not in session:
    return redirect("/")
  Ingredient.remove(recipe_id, ingredient_id)
  return redirect(f"/recipe/new")

