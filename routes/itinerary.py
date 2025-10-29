from flask import Blueprint, render_template, request, session, redirect, url_for
from markupsafe import escape
from datetime import datetime
from context import fields
from utils import functions, ai
from extensions import db
from models import ItineraryPreferences, Itinerary
from config import Config
import requests, json

itinerary = Blueprint("itinerary", __name__)
pages = fields.pages
fields = fields.itineraryfields
googleMapsKey = Config.GOOGLE_MAPS_KEY
googleMapsKeyBackend = Config.GOOGLE_MAPS_KEY_BACKEND
unsplashKey = Config.UNSPLASH_ACCESS_KEY

def get_unsplash_images(query, trip_duration):

    if unsplashKey :
        print("unsplash key found, generating")
    
    url = "https://api.unsplash.com/search/photos"
    params = {"query": query, "per_page": trip_duration, "client_id": unsplashKey}
    response = requests.get(url, params=params)

    if response.status_code == 200:
        image_urls = [r["urls"]["regular"] for r in response.json().get("results", [])]
        return image_urls
    return []

@itinerary.route("/api/place", methods=["GET"])
def get_place():
    
    existing_itinerary = Itinerary.query.get(session["itinerary_id"])
    if existing_itinerary:
        if existing_itinerary.google_places:
            return existing_itinerary.google_places, 200

    address = request.args.get("address")
    if not address:
        return {"error": "Address required"}, 400

    api_key = googleMapsKeyBackend

    geocode_url = "https://maps.googleapis.com/maps/api/geocode/json"
    geocode_params = {"address": address, "key": api_key}
    geo_res = requests.get(geocode_url, params=geocode_params).json()

    if geo_res.get("status") != "OK" or not geo_res.get("results"):
        return {"error": "Place not found"}, 404

    place_id = geo_res["results"][0]["place_id"]

    places_url = f"https://places.googleapis.com/v1/places/{place_id}"
    places_res = requests.get(
        places_url,
        headers={
            "X-Goog-Api-Key": api_key,
            "X-Goog-FieldMask": "photos"
        }
    ).json()

    photos = []
    if "photos" in places_res:
        for photo in places_res["photos"]:
            photos.append(f"https://places.googleapis.com/v1/{photo['name']}/media?maxWidthPx=800&key={api_key}")

    existing_itinerary.google_places = places_res
    db.session.commit()

    return {
        "place_id": place_id,
        "photos": photos
    }

@itinerary.route("/questionnaire")
def questionnaire():
    return render_template("questionnaire.html", pages=pages, fields=fields, current_page=request.endpoint)

@itinerary.route("/process-itinerary", methods=["POST"])
def process_itinerary():
    print("processing itinerary preferences")

    data = request.get_json()

    if "itinerary_id" in session:
        existing_preferences = ItineraryPreferences.query.get(session["itinerary_id"])
        if existing_preferences:
            return {"itinerary_id": existing_preferences.id}, 200

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
    session.permanent = True
    return {"itinerary_id": itinerary.id}, 200

@itinerary.route("/build-itinerary/<int:itinerary_id>")
def success(itinerary_id):
    existingItinerary = Itinerary.query.filter_by(preferences_id=itinerary_id).first()

    if existingItinerary:
        return {"itinerary_id": existingItinerary.id}, 200

    else:
        print("adding to database")
        itinerary = ItineraryPreferences.query.get_or_404(itinerary_id)
        preferences = functions.clean_instance(itinerary)
        itinerary_data = ai.generateItinerary(preferences)
        destination = preferences.get("destination")
        trip_duration = preferences.get("tripDuration")

        if destination:
            itinerary_data["images"] = get_unsplash_images(destination, trip_duration + 1)

        new_itinerary = Itinerary(preferences_id=itinerary_id, data=itinerary_data)
        db.session.add(new_itinerary)
        db.session.commit()

    return {"itinerary_id": new_itinerary.id}, 200

@itinerary.route("/itinerary/<int:itinerary_id>")
def display_itinerary(itinerary_id):
    existingItinerary = Itinerary.query.get_or_404(itinerary_id)
    if not existingItinerary:
        return redirect("/questionnaire")
    itineraryData = functions.decode_unicode(existingItinerary.data)
    return render_template("itinerary.html", results=itineraryData, pages=pages, googleKey = googleMapsKey)