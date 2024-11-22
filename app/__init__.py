from flask import Flask
from app.utils.config import Config 

def create_app():
    app = Flask(__name__)

    config = Config()
    app.config['CONFIG'] = config

    # Register routes
    from app.routes.routes import main
    app.register_blueprint(main)

    return app
