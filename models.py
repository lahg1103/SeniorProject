from datetime import date
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