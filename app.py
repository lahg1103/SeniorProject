from flask import *
from config import context
from utils import functions
from utils import ai
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from datetime import date, datetime, timedelta
from dotenv import load_dotenv
import os, requests

pages = context.pages
itineraryfields = context.itineraryfields
load_dotenv()

app = Flask(__name__)
app.secret_key = os.getenv('FLASK_SESSION_KEY')
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///voyage.db'
db = SQLAlchemy(app)
migrate = Migrate(app, db)
unsplashKey = os.getenv("UNSPLASH_ACCESS_KEY")


class ItineraryPreferences(db.Model):
    id = db.Column(db.Integer, primary_key=True)

    # core requirements

    budget = db.Column(db.Integer, nullable=False)
    arrivaldate = db.Column(db.Date, default=date.today)
    departuredate = db.Column(db.Date, nullable=False)
    transportation = db.Column(db.Boolean, default=True)

    # the longest city in the world is 169characters long yall.

    destination = db.Column(db.String(200), nullable=False)

    # this is just for how the row represents itself when called, makes it readable

    def __repr__(self):
        return '<Preferences %r>' % self.id

def get_unsplash_images(query, session): 
    if "unsplash_cache" not in session:
        session["unsplash_cache"] = {}
    if query in session["unsplash_cache"]:
        print(f"Using cached images for {query}")
        return session["unsplash_cache"][query]
    
    print(f"Fetching new images for {query}")
    url = "https://api.unsplash.com/search/photos"
    params = {"query": query, "per_page": 4, "client_id": unsplashKey}
    response = requests.get(url, params=params)

    if response.status_code == 200:
        results = response.json().get("results", [])
        image_urls = [p["urls"]["regular"] for p in results]
        session["unsplash_cache"][query] = image_urls
        return image_urls
    else:
        return []

@app.route('/')
def index():
    return render_template('index.html', pages=pages, current_page=request.endpoint)


@app.route('/about')
def about():
    return render_template('about.html', pages=pages, current_page=request.endpoint)


@app.route('/questionnaire')
def questionnaire():
    return render_template('questionnaire.html', pages=pages, current_page=request.endpoint, fields=itineraryfields)



@app.route('/process-itinerary', methods=['POST'])
def process_itinerary():
    data = request.get_json()

    format_string = '%Y-%m-%d'
    arrival = datetime.strptime(data['arrival_date'], format_string)
    departure = datetime.strptime(data['departure_date'], format_string)

    # Adding a new row

    itineraryUserPreferences = ItineraryPreferences(
        budget=int(data['budget']),
        arrivaldate=arrival,
        departuredate=departure,
        destination=data['destination']
    )

    # save instance

    db.session.add(itineraryUserPreferences)
    db.session.commit()

    session['itinerary_id'] = itineraryUserPreferences.id

    return ('', 204)


@app.route('/success')
def success():
    # SQLITE HERE TOO
    itinerary_id = session.get('itinerary_id')
    if not itinerary_id:
        return redirect('/questionnaire')

    if not 'itinerary' in session:

        itinerary = ItineraryPreferences.query.get_or_404(itinerary_id)

        preferences_clean = functions.clean_instance(itinerary)

        itinerary_clean = ai.generateItinerary(preferences_clean)

        session.permanent = True
        session['itinerary'] = itinerary_clean

        destination = preferences_clean.get("destination")

        if destination:
            images = get_unsplash_images(destination, session)
            itinerary_clean["images"] = images
            session['itinerary'] = itinerary_clean

        return render_template('itinerary.html', results=itinerary_clean, pages=pages)

    else:
        
        return render_template('itinerary.html', results=session["itinerary"], pages=pages)


@app.route('/contact')
def contact():
    return render_template('contact.html', pages=pages, current_page=request.endpoint)


@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html', pages=pages), 404


if __name__ == '__main__':
    # with app.app_context():
    #     db.create_all()
    app.run(debug=True)
