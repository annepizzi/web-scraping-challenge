from flask import Flask, render_template, redirect
from flask_pymongo import PyMongo
import scrape_mars

# Create an instance of Flask
app = Flask(__name__)

# setup mongo connection
mongo = PyMongo(app, uri="mongodb://localhost:27017/mars_app")

@app.route("/")
def home():

    # Find one record of data from the mongo database
    data = mongo.db.collection.find_one()
    # Return template and data
    return render_template("index.html", mars_info=data)


# Route that will trigger the scrape function
@app.route("/scrape")
def scrape():

    # Run the scrape functions
    marsData = scrape_mars.scrape_info()
    # Update the Mongo database using update and upsert=True
    mongo.db.collection.update({}, marsData, upsert=True)
    # Redirect back to home page
    return redirect("/")

if __name__ == "__main__":
    app.run(debug=True)
