from google import genai
from google.genai import types
from pydantic import BaseModel, ConfigDict
from dotenv import load_dotenv
from utils import functions
from typing import List, Literal
import json
import os

class Lodging(BaseModel):
    name: str
    address: str
    cost: int

class Meal(BaseModel):
    restaurant: str
    address: str
    cost: int

class Food(BaseModel):
    breakfast: Meal
    lunch: Meal
    dinner: Meal

class Activities(BaseModel):
    name: str
    address: str
    cost: int

class Directions(BaseModel):
    distance: str
    transportationmethod: str

class DayItinerary(BaseModel):
    lodging: Lodging
    food: Food
    activities: List[Activities]
    directions: Directions
    daysummary: str

class Itinerary(BaseModel):
    itineraryperday: List[DayItinerary]
    promotionalblurb: str
    duration : int




load_dotenv()
client = genai.Client(api_key=os.getenv("GEMINI_KEY"))

def generateItinerary(preferences):
    
    itinerary = client.models.generate_content(
        model="gemini-2.5-flash",
        config={
            "system_instruction": ("You are a travel agent expert. You are building a travel itinerary based on the following preferences listed in the dictionary. Generate realistic lodging, restaurants, timelines, etc. with the information given. Avoid generic terms like 'public transportation' be specific to the location. Avoid generic terms like 'verious locations' always be sure to pick out a specific spot."),
            # "thinking_config" : {
            #     "thinking_budget" : 0
            # },
            "response_mime_type" : "application/json",
            "response_schema": Itinerary,
        
        },
        contents=functions.stringify(preferences),
    )
    return json.loads(itinerary.text)