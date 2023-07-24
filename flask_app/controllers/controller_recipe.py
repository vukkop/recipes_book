from flask_app import app
from flask import render_template,redirect,request,session
from flask_app.models.model_user import User
from flask_app.models.model_recipe import Recipe

#create
@app.route("/recipe/new")
def new_recipe():
  if 'user_id' not in session:
    return redirect("/")
  user = User.get_by_id(session['user_id'])
  return render_template("new_recipe.html",user=user)

@app.route("/recipe/create", methods = ["POST"])
def create_recipe():
  data = {
    **request.form,
    'user_id' : session['user_id']
  }
  if 'is_favorite' not in data:
    data['is_favorite'] = 0
  # if not Recipe.validate_create(data):
  #   return redirect('/recipe/new')

  Recipe.save(data)
  return redirect('/dashboard')

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

