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
    if duration > 7:
        duration = 7
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

def scale_itinerary_costs(itinerary: dict, travelers: int) -> dict:
    def recurse(obj):
        if isinstance(obj, dict):
            new_obj = {}
            for key, value in obj.items():
                if key == "cost" and isinstance(value, int):
                    new_obj[key] = value                
                    new_obj["cost_total"] = value * travelers  
                else:
                    new_obj[key] = recurse(value)
            return new_obj

        elif isinstance(obj, list):
            return [recurse(item) for item in obj]

        else:
            return obj

    return recurse(itinerary)

if __name__ == "__main__":
    from pprint import pprint

    # Example input for testing
    test_itinerary = {
        "itineraryperday": [
            {
                "lodging": {"name": "Hotel A", "cost": 100},
                "food": {
                    "breakfast": {"restaurant": "Cafe", "cost": 10},
                    "lunch": {"restaurant": "Deli", "cost": 15},
                    "dinner": {"restaurant": "Bistro", "cost": 20}
                },
                "activities": [{"name": "Museum", "cost": 30}],
            }
        ]
    }

    num_travelers = 3
    scaled = scale_itinerary_costs(test_itinerary, num_travelers)
    pprint(scaled)
