from flask import *
from config import context
from utils import functions
from utils import ai
from flask_sqlalchemy import SQLAlchemy
from datetime import date, datetime
from dotenv import load_dotenv
import os

pages = context.pages
itineraryfields = context.itineraryfields
load_dotenv()

app = Flask(__name__)
app.secret_key = os.getenv('SESSION_KEY')
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///voyage.db'
db = SQLAlchemy(app)

class ItineraryPreferences(db.Model):
    id = db.Column(db.Integer, primary_key=True)

    #core requirements
    budget = db.Column(db.Integer, nullable=False)
    arrivaldate = db.Column(db.Date, default=date.today)
    departuredate = db.Column(db.Date, nullable=False)
    # the longest city in the world is 169characters long yall.
    destination = db.Column(db.String(200), nullable=False)

    def __repr__(self):
        return '<Preferences %r>' % self.id



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

    # REF DO SOMETHING REF TEST THE DATA REF DO SOMETHING
    # SQLITE HERE I REPEAT.

    itineraryUserPreferences = ItineraryPreferences(
        budget= int(data['budget']),
        arrivaldate= arrival,
        departuredate= departure,
        destination= data['destination']
    )

    #save instance

    db.session.add(itineraryUserPreferences)
    db.session.commit()

    session['itinerary_id'] = itineraryUserPreferences.id

    return('', 204)

@app.route('/success')
def success():
    #SQLITE HERE TOO
    itinerary_id = session.get('itinerary_id')
    if not itinerary_id:
        return redirect('/questionnaire')
    
    itinerary = ItineraryPreferences.query.get_or_404(itinerary_id)

    preferences_clean = functions.clean_instance(itinerary)

    itinerary_clean = ai.generateItinerary(preferences_clean)


    return render_template('itinerary.html', results=itinerary_clean, pages=pages)

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