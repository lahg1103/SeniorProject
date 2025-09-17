from flask import *
from config import context

pages = context.pages
itineraryfields = context.itineraryfields
data = [{'name': 'test', 'result': 'data did not update!'}]

app = Flask(__name__)

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
    # TEMPORARY WHILE IN DEVELOPMENT
    global data
    data = request.get_json()
    # REF DO SOMETHING REF TEST THE DATA REF DO SOMETHING
    print("Received itinerary:", data)
    # SQLITE HERE I REPEAT.
    return('', 204)

@app.route('/success')
def success():
    #SQLITE HERE TOO
    return render_template('itinerary.html', results=data)

@app.route('/contact')
def contact():
    return render_template('contact.html', pages=pages, current_page=request.endpoint)
    
@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html', pages=pages), 404

if __name__ == '__main__':
    app.run(debug=True)