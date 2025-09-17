

# stores template-facing data passed to Jinja templates.
pages = [{'name': 'Home', 'endpoint': 'index'},
         {'name': 'Start Planning', 'endpoint': 'questionnaire'},
         {'name': 'About', 'endpoint': 'about'},
         {'name': 'Contact', 'endpoint': 'contact'}
         ]
itineraryfields = [
    {'name': 'Budget', 'type' : 'number', 'currency' : 'USD'},
    {'name': 'Arrival Date', 'type': 'date'},
    {'name': 'Departure Date', 'type': 'date'},
    {'name': 'Destination', 'type': 'text'}
]