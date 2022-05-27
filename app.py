import datetime
import asyncio
import motor.motor_asyncio as mongodb
from pymongo.errors import ConnectionFailure
import os
from flask import Flask, render_template
from gdeltdoc import GdeltDoc, Filters
from datetime import datetime
from dateutil.relativedelta import relativedelta

TEMPLATE_DIR = os.path.abspath('templates')
STATIC_DIR = os.path.abspath('styles')
app = Flask(__name__, template_folder=TEMPLATE_DIR, static_folder=STATIC_DIR)


def mongo_ingestion():
    """Establishing Mongo Connection"""
    try:
        url = os.environ.get("MONGODB_URL", "mongodb://localhost:27017")
        client = mongodb.AsyncIOMotorClient(url)
        db = client.timeseries
        print("MongoDB connected successfully to timeseries db")
    except ConnectionFailure:
        print("Failed to connect To MongoDB")
        client.close()
    collection = db + "gdelt-collection"
    return collection

async def do_insert(dataframe_json=None):
    """Insertion into Mongo-DB"""
    collection = mongo_ingestion()
    await collection.insert_many(documents=dataframe_json)
    print("Values are Inserted Successfully !!")


@app.route("/")
def news_site():
    """ news of yesterday and today is reflected on the UI data is capture from Gdelt"""
    f = Filters(
        keyword="events",
        start_date=str(datetime.now().date()),
        end_date=str(datetime.now().date() - relativedelta(days=1))
    )
    gd = GdeltDoc()
    # Search for articles matching the filters
    data = gd.article_search(f)
    data["seendate"] = data["seendate"].apply(lambda date: date.split("T")[0])
    data["seendate"] = data["seendate"].apply(lambda date: date[0:4] + "-" + date[4:6] + "-" + date[6:])
    data.dropna(inplace=True)
    data = data[data["language"] == "English"]
    data = data.to_dict('records')
    loop = asyncio.get_event_loop()
    loop.run_until_complete(do_insert(data))
    return render_template("base.html", length=len(data), context=data)


if __name__ == "__main__":
    app.run()
