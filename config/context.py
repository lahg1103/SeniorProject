
from enum import Enum

class FoodRestrictions(Enum):
    HALAL = 'Halal'
    KOSHER = 'Kosher'
    VEGETERIAN = 'Vegetarian'
    VEGAN = 'Vegan'
    PESCATARIAN = 'Pescatarian'

class TransportationType(Enum):
    RENTAL = 'Rental'
    UBER = 'Uber'
    PUBLICTRANSPORT = 'Public Transport'
    WALKING = 'Walking'

class TripType(Enum):
    VACATION = 'Vacation'
    WORK = 'Work'
    STUDYABROAD = 'Study Abroad'

class LodgingType(Enum):
    HOTEL = 'Hotel'
    AIRBNB = 'Airbnb'
    HOSTEL = 'Hostel'

# stores template-facing data passed to Jinja templates.
pages = [{'name': 'Home', 'endpoint': 'index'},
         {'name': 'Start Planning', 'endpoint': 'questionnaire'},
         {'name': 'About', 'endpoint': 'about'},
         {'name': 'Contact', 'endpoint': 'contact'}
         ]
itineraryfields = [
    {'name': 'Budget', 'type' : 'number', 'currency' : 'USD'},
    {'name': 'Arrival Date', 'type': 'date'},
    {'name': 'Departure Date', 'type': 'date'},
    {'name': 'Destination', 'type': 'text'},

]