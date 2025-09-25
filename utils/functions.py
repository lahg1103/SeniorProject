import json

def clean_instance(instance) :
    return {
        column.name : getattr(instance, column.name)
        for column in instance.__table__.columns
        if column.name != 'id'
    }
def stringify(o) :
    return json.dumps(o, default=str)