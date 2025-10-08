from google import genai
from google.genai import types
from pydantic import BaseModel, ConfigDict
from dotenv import load_dotenv
from utils import functions
from typing import List, Literal
import json
import os

partofday = Literal["morning", "afternoon", "evening"]


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
    partofday: partofday


class Directions(BaseModel):
    distance: str
    transportationmethod: str


class TimeBlocks(BaseModel):
    morning: str
    afternoon: str
    evening: str


class DayItinerary(BaseModel):
    lodging: Lodging
    food: Food
    activities: List[Activities]
    directions: Directions
    daysummary: str
    timeblocks: TimeBlocks


class Itinerary(BaseModel):
    itineraryperday: List[DayItinerary]
    promotionalblurb: str
    duration: int
    city: str


load_dotenv()
client = genai.Client(api_key=os.getenv("GEMINI_KEY"))


def generateItinerary(preferences):

    itinerary = client.models.generate_content(
        model="gemini-2.5-flash",
        config={
            "system_instruction": ("You are a travel agent expert. You are building a travel itinerary based on the following preferences listed in the dictionary. Generate realistic lodging, restaurants, timelines, etc. with the information given. Avoid generic terms like 'public transportation' be specific to the location. Avoid generic terms like 'various locations' always be sure to pick out a specific spot. Make sure that each time block (morning, afternoon, evening) has a brief description for the meal and activity planned for that specific time block. Make sure meals are allocated to their respective time block (breakfast in the morning, lunch in the afternoon, dinner in the evening) and write a brief description of their meal, validating that it is in line with their dietary needs (if they're vegetarian validate that their meal is vegetarian). Make sure that activities are allocated to their respective time block (morning activities in the morning, afternoon activities in the afternoon, evening activities in the evening)."),
            # "thinking_config" : {
            #     "thinking_budget" : 0
            # },
            "response_mime_type": "application/json",
            "response_schema": Itinerary,

        },
        contents=functions.stringify(preferences),
    )
    return json.loads(itinerary.text)
