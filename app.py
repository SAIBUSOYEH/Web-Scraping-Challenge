
import sys
from flask import Flask, render_template, jsonify, redirect
import pymongo
import scrape_mars
sys.setrecursionlimit(2000)
app = Flask(__name__)
# the following is using local host with mongodb
client = pymongo.MongoClient()
# put home route first
@app.route("/")
def home():
    mars = client.db.mars.find_one() #this is finding data
    print(mars)
    return render_template("index.html", mars = mars)
# put scrape route second
@app.route('/scrape')
def scrape():
    mars = client.db.mars # get data again
    mars_scrape = scrape_mars.scrape() # this calls the scrape from your imported scrape_mars file
    mars.update({}, mars_scrape, upsert=True) # inserts scraped data
    return redirect("/", code=302) # redirects to home page but loads it with scraped data
if __name__ == "__main__":
    app.run(debug=True)