from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

db      = SQLAlchemy()
migrate = Migrate()


def create_app():
    app = Flask(__name__)

    from app.config.settings import Config
    app.config.from_object(Config)

    db.init_app(app)
    migrate.init_app(app, db)

    from app.routes.kitchen_routes import kitchen_bp
    app.register_blueprint(kitchen_bp, url_prefix='/api/kitchen')

    @app.get('/health')
    def health():
        return {'status': 'ok', 'service': 'kitchen-service', 'port': 8004}

    return app