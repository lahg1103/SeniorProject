from datetime import datetime

def validate_budget(budget):
    min_budget = 100  # Minimum budget (3 figures)
    max_budget = 100000  # Maximum budget (6 figures)

    if budget < min_budget:
        raise ValueError(f"Budget cannot be less than {min_budget}")
    elif budget > max_budget:
        raise ValueError(f"Budget cannot exceed {max_budget}")
    return True

def validate_location(location, valid_locations):
    if location not in valid_locations:
        raise ValueError("Invalid location")
    return True

def validate_date(date_str):
    current_date = datetime.now().date()  # date only, no time
    input_date = datetime.strptime(date_str, "%Y-%m-%d").date()  

    if input_date < current_date:
        raise ValueError("Date cannot be in the past")
    
    return True
