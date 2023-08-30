from flask import *
import routes.attractions_bp as attractions_bp
import routes.mrts_bp as mrts_bp
app=Flask(__name__)
app.config["JSON_AS_ASCII"]=False
app.config["TEMPLATES_AUTO_RELOAD"]=True
app.config.from_object("config")

# Register blueprints
#/api/attractions
app.register_blueprint(attractions_bp.blueprints)
#/api/mrts
app.register_blueprint(mrts_bp.blueprints)


# Pages
@app.route("/")
def index():
	return render_template("index.html")
@app.route("/attraction/<id>")
def attraction(id):
	return render_template("attraction.html")
@app.route("/booking")
def booking():
	return render_template("booking.html")
@app.route("/thankyou")
def thankyou():
	return render_template("thankyou.html")

app.run(host="127.0.0.1", port=3000)