from flask import Blueprint, render_template, request, session, redirect, url_for, jsonify, current_app
from markupsafe import escape
from datetime import datetime
from context import fields
from utils import functions, ai, weather_api
from extensions import db
from models import ItineraryPreferences, Itinerary
from config import Config
from threading import Thread
import requests, json

itinerary = Blueprint("itinerary", __name__)
pages = fields.pages
fields = fields.itineraryfields
googleMapsKey = Config.GOOGLE_MAPS_KEY
googleMapsKeyBackend = Config.GOOGLE_MAPS_KEY_BACKEND
unsplashKey = Config.UNSPLASH_ACCESS_KEY


def get_unsplash_images(query, trip_duration):

    if unsplashKey:
        print("unsplash key found, generating")
    else:
        return []

    try:
        url = "https://api.unsplash.com/search/photos"
        params = {"query": query, "per_page": trip_duration,
                  "client_id": unsplashKey}
        response = requests.get(url, params=params)

        if response.status_code == 200:
            image_urls = [r["urls"]["regular"]
                          for r in response.json().get("results", [])]
            return image_urls
        return []
    except Exception as e:
        print(f"Error fetching images from Unsplash: {e}")
        return []

def build_itinerary_task(app, itinerary_id):
    with app.app_context():
        try:
            print(f"Building itinerary for preferences_id={itinerary_id}")
            itineraryPreferences = ItineraryPreferences.query.get_or_404(itinerary_id)
            itinerary = Itinerary.query.filter_by(preferences_id=itinerary_id).one_or_none()
            if not itinerary:
                itinerary = Itinerary()
                itinerary.preferences_id = itinerary_id
                db.session.add(itinerary)

            preferences = functions.clean_instance(itineraryPreferences)
            itinerary_data = ai.generateItinerary(preferences)
            destination = preferences.get("destination")
            trip_duration = preferences.get("tripDuration")
            
            images = []

            if destination:
                images = get_unsplash_images(destination, trip_duration + 1)

            itinerary.data = itinerary_data
            itinerary.images = images 

            db.session.commit()
            print(f"Itinerary updated: id={itinerary.id}, preferences_id={itinerary_id}")


        except Exception as e:
            print("Error generating itinerary: ", e)

def process_preferences(data, existing=None):
    arrival = datetime.strptime(data["arrival_date"], "%Y-%m-%d")
    departure = datetime.strptime(data["departure_date"], "%Y-%m-%d")

    itinerary = existing if existing else ItineraryPreferences()
    itinerary.numberOfTravelers=int(data["number_of_travelers"])
    itinerary.budget=int(data["budget"])
    itinerary.arrivaldate=arrival
    itinerary.departuredate=departure
    itinerary.destination=escape(data.get("destination", "").strip())
    itinerary.foodBudget=int(data["foodBudget"])
    itinerary.lodgingBudget=int(data["lodgingBudget"])
    itinerary.transportationBudget=int(data["transportationBudget"])
    itinerary.activityBudget=int(data["activityBudget"])
    itinerary.tripDuration=functions.trip_duration(arrival, departure)
    weather = []
    try:
        weather = weather_api.get_weather_itinerary(
                destination=data.get("destination"),
                arrival_date=arrival,
                departure_date=departure
            )
    except Exception as e:
            import traceback; traceback.print_exc()
            weather = {
                "source": "none",
                "days": [],
                "location": data.get("destination")
            }

    itinerary.weather=weather

    return itinerary
        

@itinerary.route("/api/place", methods=["GET"])
def get_place():

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
            photos.append(
                f"https://places.googleapis.com/v1/{photo['name']}/media?maxWidthPx=800&key={api_key}")

    return {
        "place_id": place_id,
        "photos": photos
    }

@itinerary.route("/questionnaire")
def questionnaire():
    itinerary_id = request.args.get("itinerary_id")
    existing = None

    if itinerary_id:
        existing = ItineraryPreferences.query.get(itinerary_id)

    return render_template("questionnaire.html",
                            pages=pages,
                            fields=fields,
                            current_page=request.endpoint,
                            existing=existing,
                            update_mode=bool(existing)
                            )


@itinerary.route("/process-itinerary", methods=["POST"])
def process_itinerary():
    print("processing itinerary preferences")

    try:
        data = request.get_json()
        itinerary_id = data.get("itinerary_id") or session.get("itinerary_id")

        
        existing = None

        if itinerary_id:
            existing = ItineraryPreferences.query.get(itinerary_id)

        itinerary = process_preferences(data, existing)

        if not existing:
            db.session.add(itinerary)
        
        db.session.commit()

        session["itinerary_id"] = itinerary.id
        session.permanent = True

        return {"itinerary_id": itinerary.id}, 200
    
    except Exception as e:
        print(str(e))
        return{"error": str(e)}, 500 



@itinerary.route("/build-itinerary/<int:itinerary_id>")
def success(itinerary_id):
    app = current_app._get_current_object()
    Thread(target=build_itinerary_task, args=(app,itinerary_id)).start()
    return jsonify({"status": "processing",
                    "itinerary_id": itinerary_id}), 200

@itinerary.route("/itinerary-status/<int:itinerary_id>")
def itinerary_status(itinerary_id):
    print("SESSION:", session.get("itinerary_id"))
    itinerary = Itinerary.query.filter_by(preferences_id=itinerary_id).first()
    if itinerary:
        return jsonify({"status": "ready", "itinerary_id": itinerary.id})
    return jsonify({"status": "processing"})


@itinerary.route("/itinerary/<int:itinerary_id>")
def display_itinerary(itinerary_id):

    existingItinerary = Itinerary.query.get(itinerary_id)

    existingPreferences = ItineraryPreferences.query.get(itinerary_id)
    # travelers = existingPreferences.numberOfTravelers if existingPreferences else 1

    # remember to come back and do something with this lol
    #scale costs


    #fix images
    unsplashPhotos = existingItinerary.images
    weatherData = existingPreferences.weather or None

    if not existingItinerary:
        session.pop("itinerary_id", None)
        return redirect("/questionnaire")
    
    itineraryData = functions.decode_unicode(existingItinerary.data)

    return render_template("itinerary.html", results=itineraryData, pages=pages, googleKey=googleMapsKey, photos=unsplashPhotos, existingPreferences=existingPreferences, weather= weatherData)
