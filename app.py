from flask import *

app = Flask(__name__)

pages = [{'name': 'About', 'endpoint': 'about'},
         {'name': 'Home', 'endpoint': 'index'},
         {'name': 'Start Planning', 'endpoint': 'questionnaire'},
         {'name': 'Contact', 'endpoint': 'contact'},
         {'name': 'FAQ', 'endpoint': 'FAQ'},
         {'name': 'Philosophy', 'endpoint': 'philosophy'}]

@app.route('/')
def index():
    return render_template('index.html', pages=pages, current_page=request.endpoint)

@app.route('/about')
def about():
    return render_template('about.html', pages=pages, current_page=request.endpoint)

@app.route('/questionnaire')
def questionnaire():
    return render_template('questionnaire.html', pages=pages, current_page=request.endpoint)

@app.route('/FAQ')
def FAQ():
    return render_template('faq.html', pages=pages, current_page=request.endpoint)

@app.route('/philosophy')
def philosophy():
    return render_template('philosophy.html', pages=pages, current_page=request.endpoint)

@app.route('/contact')
def contact():
    return render_template('contact.html', pages=pages, current_page=request.endpoint)

if __name__ == '__main__':
    app.run(debug=True)