from flask import Blueprint, render_template, request
from context import fields

main = Blueprint("main", __name__)
pages = fields.pages

@main.route("/")
def index():
    return render_template("index.html", pages=pages, current_page=request.endpoint)

@main.route("/about")
def about():
    return render_template("about.html", pages=pages, current_page=request.endpoint)

@main.route("/contact")
def contact():
    return render_template("contact.html", pages=pages, current_page=request.endpoint)