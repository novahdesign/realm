from flask import Flask

def create_app():
    app = Flask(__name__)

    # Register blueprints
    from .main import main as main_blueprint
    from .main import auth as auth_blueprint
    
    app.register_blueprint(main_blueprint)
    app.register_blueprint(auth_blueprint)

    return app
