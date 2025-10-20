from flask import Flask, render_template
from config import Config
from extensions import db, migrate
from routes.main import main
from routes.itinerary import itinerary

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
    @app.errorhandler(404)
    def not_found(e):
        return render_template("404.html"), 404

    return app

app = create_app()

if __name__ == "__main__":
    app = create_app()
    port = int(Config.PORT or 8000)
    app.run(host="0.0.0.0", port=port)
