import json
from datetime import datetime


def clean_instance(instance) :
    return {
        column.name : getattr(instance, column.name)
        for column in instance.__table__.columns
        if column.name != 'id'
    }
def stringify(o) :
    return json.dumps(o, default=str)

def trip_duration(arrival_date, departure_date):
    duration = (departure_date - arrival_date).days + 1
    return max(duration, 0)

