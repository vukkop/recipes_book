from flask_app import app
from flask import render_template,redirect,session

@app.route("/")
def index():
  if 'user_id' in session:
    return redirect("/dashboard")
  return render_template("index.html")

@app.route("/sign_up")
def sign_up():
  if 'user_id' in session:
    return redirect("/dashboard")
  return render_template("sign_up.html")



