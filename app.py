from flask import *
from config import context

pages = context.pages
itinerary_form_fields = context.itinerary_form_fields

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html', pages=pages, current_page=request.endpoint)

@app.route('/about')
def about():
    return render_template('about.html', pages=pages, current_page=request.endpoint)

@app.route('/questionnaire')
def questionnaire():
    return render_template('questionnaire.html', pages=pages, current_page=request.endpoint)

@app.route('/contact')
def contact():
    return render_template('contact.html', pages=pages, current_page=request.endpoint)
    
@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html', pages=pages), 404

if __name__ == '__main__':
    app.run(debug=True)