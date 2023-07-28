from flask_app import app
from flask import render_template,redirect,request,session
from flask_app.models.model_ingredient import Ingredient
from flask_app.models.model_user import User
from flask_app.models.model_recipe import Recipe
from flask_app.models.model_shopping_list import Shopping_List


#create
# @app.route("/ingredient/create", methods = ["POST"])
# def create_ingredient():
#   data = {
#     **request.form,
#     'user_id' : session['user_id']
#   }


#   Ingredient.save(data)
#   return redirect('/ingredients')

#read
@app.route("/shopping_list")
def shopping_list():
  if 'user_id' not in session:
    return redirect("/")
  user = User.get_by_id(session['user_id'])
  shopping_list = Shopping_List.get_by_user_id(session['user_id'])
  return render_template("display_shopping_list.html", user=user, shopping_list=shopping_list )

@app.route("/shopping_list/add/<int:recipe_id>")
def add_to_shopping_list(recipe_id):
  if 'user_id' not in session:
    return redirect("/")
  Shopping_List.save(recipe_id)


  return redirect(f"/shopping_list")






#delete
# @app.route("/ingredient/<int:id>/delete")
# def delete_ingredient(id):
#   if 'user_id' not in session:
#     return redirect("/")
#   Ingredient.delete(id)
#   return redirect("/ingredients")

# @app.route("/recipe/edit/<int:recipe_id>/ingredient/<int:ingredient_id>/remove")
# def remove_ingredient_edit(recipe_id, ingredient_id):
#   if 'user_id' not in session:
#     return redirect("/")
#   Ingredient.remove(recipe_id, ingredient_id)
#   return redirect(f"/recipe/edit/{recipe_id}")

# @app.route("/recipe/new/<int:recipe_id>/ingredient/<int:ingredient_id>/remove")
# def remove_ingredient_new(recipe_id, ingredient_id):
#   if 'user_id' not in session:
#     return redirect("/")
#   Ingredient.remove(recipe_id, ingredient_id)
#   return redirect(f"/recipe/new")

