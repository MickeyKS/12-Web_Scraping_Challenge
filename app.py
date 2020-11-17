#Import Dependencies
from flask import Flask, render_template, redirect
from flask_pymongo import PyMongo
import os
import scrape_mars
import pymongo

#Create Flask
app = Flask(__name__)

#Establish Mongo Connection
mongo = PyMongo(app, uri="mongodb://localhost:27017/mars_app")

#Render route using Pymongo
@app.route("/")
def home():

    #Find Data
    mars = mongo.db.mars.find_one()

    #Return Template
    return render_template("index.html", mars=mars)

#Route to Scrape
@app.route("/scrape")
def scrape():

    #Define Database and Collection
    mars = mongo.db.mars

    #Call scrape_data Function in scrape_mars.py
    mars_data = scrape_mars.scrape_data()

    #Updating Collection 
    mars.update({}, mars_data, upsert=True)

    #Redirect to Homepage
    return redirect("/")

if __name__ == "__main__":
    app.run(debug=True)
