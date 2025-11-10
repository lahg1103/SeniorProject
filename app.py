from flask import Flask, render_template
from config import Config
from extensions import db, migrate
from routes.main import main
from routes.itinerary import itinerary
from context import fields

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    # Initialize extensions
    db.init_app(app)
    migrate.init_app(app, db)

    # Register blueprints
    app.register_blueprint(main)
    app.register_blueprint(itinerary)

    # CLI command for db init
    @app.cli.command("init-db")
    def init_db():
        """Initialize the database"""
        with app.app_context():
            db.create_all()
            print("✅ Database initialized successfully")

    # Error handler
    @app.errorhandler(Exception)
    def handle_exception(e):
        code = getattr(e, 'code', 500)
        message = getattr(e, 'description', str(e))
        return render_template("errors.html", code=code, message=message, pages=fields.pages), code

    return app


if __name__ == "__main__":
    app = create_app()
    port = int(Config.PORT or 8000)
    app.run(host="0.0.0.0", port=port)
