from datetime import date, datetime, timezone
from extensions import db

class ItineraryPreferences(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    budget = db.Column(db.Integer, nullable=False)
    arrivaldate = db.Column(db.Date, default=date.today)
    departuredate = db.Column(db.Date, nullable=False)
    foodBudget = db.Column(db.Integer, nullable=False)
    lodgingBudget = db.Column(db.Integer, nullable=False)
    transportationBudget = db.Column(db.Integer, nullable=False)
    activityBudget = db.Column(db.Integer, nullable=False)
    tripDuration = db.Column(db.Integer, nullable=True)
    destination = db.Column(db.String(200), nullable=False)

    def __repr__(self):
        return f"<Preferences {self.id}>"
    
class Itinerary(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    preferences_id = db.Column(db.Integer, db.ForeignKey("itinerary_preferences.id"), nullable=False)
    data = db.Column(db.JSON, nullable=False)
    images = db.Column(db.JSON, nullable=True)
    google_places = db.Column(db.JSON, nullable=True)
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))

    preferences = db.relationship("ItineraryPreferences", backref=db.backref("itinerary", uselist=False, cascade="all, delete"))

    def __repr__(self):
        return f"<Itinerary for Prefs {self.preferences_id}>"