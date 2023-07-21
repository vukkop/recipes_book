from flask_app import app
from flask import render_template,redirect,request,session
from flask_app.models.model_user import User
from flask_app.models.model_recipe import Sighting

#create
@app.route("/new/sighting")
def new_sighting():
  if 'user_id' not in session:
    return redirect("/")
  user = User.get_by_id(session['user_id'])
  return render_template("new_sighting.html",user=user)

@app.route("/sighting/create", methods = ["POST"])
def create_sighting():
  data = {
    **request.form,
    'user_id' : session['user_id']
  }
  if not Sighting.validate_create(data):
    return redirect('new/sighting')

  Sighting.save(data)
  return redirect('/dashboard')

#read
@app.route("/show/<int:id>")
def display_sighting(id):
  if 'user_id' not in session:
    return redirect("/")
  user = User.get_by_id(session['user_id'])
  sighting = Sighting.get_one(id)
  return render_template("display_sighting.html", sighting=sighting, user=user)

#update
@app.route("/edit/<int:id>")
def edit_sighting(id):
  if 'user_id' not in session:
    return redirect("/")
  user = User.get_by_id(session['user_id'])
  sighting = Sighting.get_by_id(id)
  return render_template("edit_sighting.html", sighting=sighting, user=user)

@app.route("/sighting/<int:id>/update", methods = ["POST"])
def update_sighting(id):
  if 'user_id' not in session:
    return redirect("/")
  data = {
    **request.form,
    'id': id}
  if not Sighting.validate_create(data):
    return redirect(f'/sightings/{id}/edit')
  Sighting.update(data)
  return redirect("/dashboard")

#delete
@app.route("/sighting/<int:id>/delete")
def delete_sighting(id):
  if 'user_id' not in session:
    return redirect("/")
  Sighting.delete(id)
  return redirect("/dashboard")

