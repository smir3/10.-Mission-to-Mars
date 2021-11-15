#use flask to render a template, redirect to another url and create a url
from flask import Flask, render_template, redirect, url_for
#use PyMongo to interact with Mongo database
from flask_pymongo import PyMongo
#use scraping mode by converting from jupyter notebook to python
import scraping

# Set up Flask
app = Flask(__name__)

# Use flask_pymongo to set up mongo connection
#app will connect to Mongo using URI, uniform resource identifier similar to a URL
app.config["MONGO_URI"] = "mongodb://localhost:27017/mars_app"
mongo = PyMongo(app)

#Below code links visual representation of work, web app, to the code that powers it: use index.html as the default html that well use to display the content weve scraped. mars = used PyMongo to find the mars collection in the database. return render_template tells flask to return an html template using an index.html file. mars=mars tells python to use the mars collection in MongoDB
@app.route("/")
def index():
   mars = mongo.db.mars.find_one()
   return render_template("index.html", mars=mars)

#set up the scraping route which will be the button of the web application which will scrape updated data from the homepage of our web app
#first line defines the route that flask will be using, define the function def scrape(), assign a new variable that points to Mongo Database mars = mongo.db.mars, hold the newly scraped data mars_data = scraping.scrape_all() this is referencing the scrape_all function int he scraping.py file from jupyter notebook, update the database using .update()
@app.route("/scrape")
def scrape():
   mars = mongo.db.mars
   mars_data = scraping.scrape_all()
   mars.update({}, mars_data, upsert=True)
   return redirect('/', code=302)

#flask run
if __name__ == "__main__":
   app.run()
