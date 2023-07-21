from flask_app import app

from flask_app.controllers import controller_recipe, controller_routes, controller_user

if __name__ == "__main__":
    app.run(debug=True)

