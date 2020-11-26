"""Initialize Flask app."""
import os
import yaml
from flask import Flask
from flask_assets import Environment
import logging.config

def setup_logging(default_path='webapp/logging.yaml', default_level=logging.INFO, env_key='LOG_CFG'):
    path = default_path
    value = os.getenv(env_key, None)
    if value:
        path = value
    if os.path.exists(path):
        with open(path, 'rt') as f:
            try:
                config = yaml.safe_load(f.read())
                logging.config.dictConfig(config)
            except Exception as e:
                print(e)
                print('Error in Logging Configuration. Using default configs')
                logging.basicConfig(level=default_level)
    else:
        logging.basicConfig(level=default_level)
        print('Failed to load configuration file. Using default configs:'+ path)

def init_app():
    """Create Flask application."""
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_object("config.Config")
    assets = Environment()
    assets.init_app(app)

    setup_logging()

    with app.app_context():
        # Import parts of our application
        from .assets import compile_static_assets
        from .dashboard import dashboard
        from .indicators import indicators
        from .admin import admin
        # from .strategies import strategies
        # from .prediction import prediction
        # from .symbols import symbols
        # from .profile import profile

        # Register Blueprints
        app.register_blueprint(admin.admin_bp, url_prefix='/admin')
        app.register_blueprint(dashboard.dashboard_bp, url_prefix='/')
        app.register_blueprint(indicators.indicators_bp, url_prefix='/indicators')
        # app.register_blueprint(candlestickpattern.candlestickpattern_bp)

        # Compile static assets
        compile_static_assets(assets)

        return app