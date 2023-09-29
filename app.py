from flask import *
import routes.attractions_bp as attractions_bp
import routes.mrts_bp as mrts_bp
import routes.user_bp as user_bp
import routes.booking_bp as booking_bp
import sys
sys.path.insert(1, './')
from werkzeug.exceptions import HTTPException
app=Flask(__name__)
app.config["JSON_AS_ASCII"]=False
app.config["TEMPLATES_AUTO_RELOAD"]=True
app.config.from_object("config")
app.json.ensure_ascii = False

# Register blueprints
#/api/attractions
app.register_blueprint(attractions_bp.blueprints_v1)
app.register_blueprint(attractions_bp.blueprints_v2)

#/api/mrts
app.register_blueprint(mrts_bp.blueprints)
#/api/user
app.register_blueprint(user_bp.blueprints)
#/api/booking
app.register_blueprint(booking_bp.blueprints)


app.config
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



def main():
	try:
		app.run(host="0.0.0.0",port=3000)
	except Exception as err:
		print(err)
		main()


if __name__=="__main__":
	main()