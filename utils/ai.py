from google import genai
from google.genai import types
from dotenv import load_dotenv
from utils import functions
import os

load_dotenv()
client = genai.Client(api_key=os.getenv("GEMINI_KEY"))

def generateItinerary(preferences):
    
    itinerary = client.models.generate_content(
        model="gemini-2.5-flash",
        config=types.GenerateContentConfig(
            system_instruction="You are a travel agent expert. You are building a travel itinerary based on the following preferences listed in the dictionary. Generate realistic lodging, restaurants, timelines, etc. with the information given.",
            thinking_config=types.ThinkingConfig(thinking_budget=0)
        ),
        contents=functions.stringify(preferences), 
    )
    return itinerary.text