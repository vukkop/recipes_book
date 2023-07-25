from flask_app import app

from flask_app.controllers import controller_recipe, controller_routes, controller_user, controller_ingredient

if __name__ == "__main__":
    app.run(debug=True)

