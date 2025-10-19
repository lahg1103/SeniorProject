from flask import Blueprint, render_template, request, session, redirect
from markupsafe import escape
from datetime import datetime
from context import fields
from utils import functions, ai
from extensions import db
from models import ItineraryPreferences
import requests, os

itinerary = Blueprint("itinerary", __name__)
pages = fields.pages
fields = fields.itineraryfields
unsplashKey = os.getenv("UNSPLASH_ACCESS_KEY")

def get_unsplash_images(query, session, trip_duration):
    if "unsplash_cache" not in session:
        session["unsplash_cache"] = {}
    if query in session["unsplash_cache"]:
        return session["unsplash_cache"][query]

    url = "https://api.unsplash.com/search/photos"
    params = {"query": query, "per_page": trip_duration, "client_id": unsplashKey}
    response = requests.get(url, params=params)
    if response.status_code == 200:
        image_urls = [r["urls"]["regular"] for r in response.json().get("results", [])]
        session["unsplash_cache"][query] = image_urls
        return image_urls
    return []

@itinerary.route("/questionnaire")
def questionnaire():
    return render_template("questionnaire.html", pages=pages, fields=fields, current_page=request.endpoint)

@itinerary.route("/process-itinerary", methods=["POST"])
def process_itinerary():
    print("processing itinerary preferences")
    data = request.get_json()
    arrival = datetime.strptime(data["arrival_date"], "%Y-%m-%d")
    departure = datetime.strptime(data["departure_date"], "%Y-%m-%d")

    itinerary = ItineraryPreferences(
        budget=int(data["budget"]),
        arrivaldate=arrival,
        departuredate=departure,
        destination=escape(data.get("destination", "").strip()),
        foodBudget=int(data["foodBudget"]),
        lodgingBudget=int(data["lodgingBudget"]),
        transportationBudget=int(data["transportationBudget"]),
        activityBudget=int(data["activityBudget"]),
        tripDuration=functions.trip_duration(arrival, departure),
    )

    db.session.add(itinerary)
    db.session.commit()
    session["itinerary_id"] = itinerary.id
    return ("", 204)

@itinerary.route("/success")
def success():
    itinerary_id = session.get("itinerary_id")
    if not itinerary_id:
        return redirect("/questionnaire")

    if "itinerary" not in session:
        print("creating session")
        itinerary = ItineraryPreferences.query.get_or_404(itinerary_id)
        preferences = functions.clean_instance(itinerary)
        itinerary_data = ai.generateItinerary(preferences)
        destination = preferences.get("destination")
        trip_duration = preferences.get("tripDuration")

        if destination:
            itinerary_data["images"] = get_unsplash_images(destination, session, trip_duration + 1)

        session.permanent = True
        session["itinerary"] = itinerary_data

    return render_template("itinerary.html", results=session["itinerary"], pages=pages)