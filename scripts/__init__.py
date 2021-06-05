import os

from flask import Flask

def create_app():

	app = Flask(__name__)

	#app.config.from_pyfile("config.py")
	app.config.from_mapping(
		#DATABASE=os.path.join(app.instance_path, "chars.sqlite")
		SECRET_KEY="dev",
		DATABASE="scripts/chars.sqlite"
	)

	#@app.route("/")
	#def factory_hi():
	#	return("Made from app factory")

	from . import database
	database.init_app(app)

	from . import auth
	app.register_blueprint(auth.bp)

	from . import main
	app.register_blueprint(main.bp)
	app.add_url_rule("/", endpoint="index")

	return app