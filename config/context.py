

# stores template-facing data passed to Jinja templates.
pages = [{'name': 'Home', 'endpoint': 'index'},
         {'name': 'Start Planning', 'endpoint': 'questionnaire'},
         {'name': 'About', 'endpoint': 'about'},
         {'name': 'Contact', 'endpoint': 'contact'}
         ]
itinerary_form_fields = [
    {'name': 'Budget', 'type' : 'number', 'currency' : 'USD'}
]