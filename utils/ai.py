from google import genai
from google.genai import types
from pydantic import BaseModel, ConfigDict, Field
from dotenv import load_dotenv
from utils import functions
from typing_extensions import Annotated
from typing import List, Literal
import json
import os


class Lodging(BaseModel):
    name: str
    address: str
    cost: str = Field(description="number and currency")


class Meal(BaseModel):
    restaurant: str
    address: str
    cost: str = Field(description="number and currency")


class Food(BaseModel):
    breakfast: Meal
    lunch: Meal
    dinner: Meal


class Activities(BaseModel):
    name: str
    address: str
    cost: str = Field(description="number and currency")
    time: str = Field(
        description="Give me a short, evocative label for this timeblock—just an article, an adjective, and a noun. No full sentences.")
    summary: str


class Directions(BaseModel):
    distance: str
    transportationmethod: str


class TimeBlocks(BaseModel):
    morning: Annotated[List[Activities], Field(
        min_items=1, max_items=1, description="The list of activities for the morning")]
    afternoon: Annotated[List[Activities], Field(
        min_items=1, max_items=1, description="The list of activities for the morning")]
    evening: Annotated[List[Activities], Field(
        min_items=1, max_items=1, description="The list of activities for the morning")]


class DayItinerary(BaseModel):
    lodging: Lodging
    food: Food
    directions: Directions
    daysummary: str
    timeblocks: TimeBlocks


class Itinerary(BaseModel):
    itineraryperday: List[DayItinerary]
    promotionalblurb: str
    tripduration: int = Field(
        description="an integer value representing the length in days of the trip")
    city: str


load_dotenv()

api_key = os.environ.get("GEMINI_KEY") or os.getenv("GEMINI_KEY")

client = genai.Client(api_key=api_key)


def generateItinerary(preferences, weather=None):
    print("generating itinerary")
    payload = {
        "preferences": preferences,
        "weather": weather
    }
    try:
        itinerary = client.models.generate_content(
            model="gemini-2.5-flash",
            config={
<<<<<<< HEAD
                "system_instruction": ("You are a travel agent expert. You are building a travel itinerary based on the following preferences listed. Generate realistic lodging, restaurants, timelines, etc. with the information given. There is an input field for the number of traveler's. Verify that each traveler is being accounted for and adjust lodging, meals, transportation, and activities accordingly if there is  more than 1 traveler. When travelers are more than 1 use terms like 'group activities' or 'eat together' to validate that it's more than one traveler on the trip. Interpret the total budget as being for the entire group. Avoid generic terms like 'public transportation' be specific to the location. Avoid generic terms like 'various locations' always be sure to pick out a specific spot. Make sure that each time block (morning, afternoon, evening) has a brief, editorial description for the meal and activity planned for that specific time block. Make sure meals are allocated to their respective time block (breakfast in the morning, lunch in the afternoon, dinner in the evening) and write a brief description of their meal, validating that it is in line with their dietary needs (if they're vegetarian validate that their meal is vegetarian). Make sure that activities are allocated to their respective time block (morning activities in the morning, afternoon activities in the afternoon, evening activities in the evening). Take weather into account, recommend appropriate activities and clothing for each day and time block. If weather is hot, recommend cool activities and appropriate clothing. If there is rain recommend indoor activities and appropriate clothing. If it is cold, recommend apporpriate clothing and activities based on the weather."),
=======
                "system_instruction": ("You are a travel agent expert. You are building a travel itinerary based on the following preferences listed. Generate realistic lodging, restaurants, timelines, etc. with the information given. There is an input field for the number of traveler's. Verify that each traveler is being accounted for and adjust lodging, meals, transportation, and activities accordingly if there is  more than 1 traveler. When travelers are more than 1 use terms like 'group activities' or 'eat together' to validate that it's more than one traveler on the trip. Interpret the total budget as being for the entire group. Avoid generic terms like 'public transportation' be specific to the location. Avoid generic terms like 'various locations' always be sure to pick out a specific spot. Make sure that each time block (morning, afternoon, evening) has a brief, editorial description for the meal and activity planned for that specific time block. Make sure meals are allocated to their respective time block (breakfast in the morning, lunch in the afternoon, dinner in the evening) and write a brief description of their meal, validating that it is in line with their dietary needs (if they're vegetarian validate that their meal is vegetarian). Make sure that activities are allocated to their respective time block (morning activities in the morning, afternoon activities in the afternoon, evening activities in the evening). Take weather into account, recommend appropriate activities and clothing for each day and time block. If weather is hot, recommend cool activities and appropriate clothing. If there is rain, recommend indoor activities and appropriate clothing. If it is cold, recommend appropriate clothing and activities based on the weather."),
>>>>>>> updated ai model to take weather into account
                "thinking_config": {
                    "thinking_budget": 0
                },
                "response_mime_type": "application/json",
                "response_schema": Itinerary,

            },
            contents=functions.stringify(payload),
        )
        return json.loads(itinerary.text)
    except Exception as e:
        return "Error: {e}"
