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

def decode_unicode(obj):
    if isinstance(obj, dict):
        return {k: decode_unicode(v) for k, v in obj.items()}
    elif isinstance(obj, list):
        return [decode_unicode(i) for i in obj]
    elif isinstance(obj, str):
        return obj.encode('utf-8').decode('unicode_escape')
    else:
        return obj
