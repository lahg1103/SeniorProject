import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import pytest
from utils.validators import validate_budget, validate_location, validate_date
from datetime import datetime, timedelta

def test_validate_budget():
    # Test for valid budgets (within the 3 to 6 figure range)
    assert validate_budget(100)  # Exactly the minimum budget
    assert validate_budget(5000)  # A valid budget within the range
    assert validate_budget(999999)  # A valid budget within the range

    # Test for invalid budgets
    with pytest.raises(ValueError):
        validate_budget(50)  # Below the minimum budget (invalid)

    with pytest.raises(ValueError):
        validate_budget(1500000)  # Above the maximum budget (invalid)

def test_validate_location():
    valid_locations = ['New York', 'San Francisco', 'Los Angeles']
    
    # Test for valid location
    assert validate_location('New York', valid_locations)

    # Test for invalid location
    with pytest.raises(ValueError):
        validate_location('Chicago', valid_locations)

def test_validate_date():
    future_date = (datetime.now() + timedelta(days=1)).strftime("%Y-%m-%d")
    past_date = (datetime.now() - timedelta(days=1)).strftime("%Y-%m-%d")

    # Test for valid dates (future or present)
    assert validate_date(future_date)
    assert validate_date(datetime.now().strftime("%Y-%m-%d"))

    # Test for invalid dates (past date)
    with pytest.raises(ValueError):
        validate_date(past_date)
