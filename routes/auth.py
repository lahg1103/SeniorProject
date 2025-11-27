from flask import Blueprint, render_template, request, redirect, url_for, session
from werkzeug.security import generate_password_hash, check_password_hash

from extensions import db
from models import User, ItineraryPreferences, Itinerary

auth = Blueprint("auth", __name__)

@auth.route("/register", methods=["GET", "POST"])
def register():
    error = None
    if request.method == "POST":
        email = request.form["email"].strip().lower()
        password = request.form["password"]
        confirm = request.form["confirm_password"]

        if password != confirm:
            error = "Passwords do not match."
        elif User.query.filter_by(email=email).first():
            error = "An account with that email already exists."
        else:
            user = User(
                email=email,
                password_hash=generate_password_hash(password),
            )
            db.session.add(user)
            db.session.commit()

            session["user_id"] = user.id
            return redirect(url_for("itinerary.questionnaire"))

    return render_template("register.html", error=error)


@auth.route("/login", methods=["GET", "POST"])
def login():
    error = None
    if request.method == "POST":
        email = request.form["email"].strip().lower()
        password = request.form["password"]

        user = User.query.filter_by(email=email).first()
        if not user or not check_password_hash(user.password_hash, password):
            error = "Invalid email or password."
        else:
            session["user_id"] = user.id
            return redirect(url_for("itinerary.questionnaire"))

    return render_template("login.html", error=error)


@auth.route("/logout")
def logout():
    session.pop("user_id", None)
    session.pop("itinerary_id", None)  # optional
    return redirect(url_for("main.index"))


@auth.route("/my-itineraries")
def my_itineraries():
    user_id = session.get("user_id")
    if not user_id:
        return redirect(url_for("auth.login"))

    # Join preferences with itineraries so we know which are built
    results = (
        db.session.query(ItineraryPreferences, Itinerary)
        .outerjoin(Itinerary, Itinerary.preferences_id == ItineraryPreferences.id)
        .filter(ItineraryPreferences.user_id == user_id)
        .order_by(ItineraryPreferences.arrivaldate.desc())
        .all()
    )

    itineraries = []
    for pref, itin in results:
        itineraries.append({
            "itinerary_id": itin.id if itin else None,
            "preferences_id": pref.id,
            "destination": pref.destination,
            "arrivaldate": pref.arrivaldate,
            "departuredate": pref.departuredate,
            "budget": pref.budget,
        })

    return render_template("my_itineraries.html", itineraries=itineraries)