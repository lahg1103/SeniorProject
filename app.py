from flask import *
from config.context import *

app = Flask(__name__)

pages = [{'name': 'Home', 'endpoint': 'index'},
         {'name': 'Start Planning', 'endpoint': 'questionnaire'},
         {'name': 'About', 'endpoint': 'about'},
         {'name': 'Contact', 'endpoint': 'contact'}
         ]

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