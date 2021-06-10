from flask import Flask, render_template, redirect
from flask_pymongo import PyMongo
import scrape_mars

# Create an instance of our Flask app.
app = Flask(__name__)

# Use flask_pymongo to set up mongo connection
app.config["MONGO_URI"] = "mongodb://localhost:27017/mars_app"
mongo = PyMongo(app)


@app.route("/")
def index():
    data_dict = mongo.db.data_dict.find_one()
    return render_template("index.html", data=data_dict)

@app.route("/scrape")
def scrape():
    data_dict = mongo.db.data_dict
    mars_data = scrape_mars.scrape()
    data_dict.update({}, mars_data, upsert=True)
    return redirect("/", code=302)

if __name__ == "__main__":
    app.run(debug=True)