from flask import Flask, render_template, redirect, url_for
from config import Config
from extensions import db, bcrypt, login_manager

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    # Initialize extensions
    db.init_app(app)
    bcrypt.init_app(app)
    login_manager.init_app(app)

    # Configure Login Manager
    login_manager.login_view = 'auth.login'
    login_manager.login_message = 'Please log in to access this page.'
    login_manager.login_message_category = 'warning'

    # User loader callback for Flask-Login
    from models.models import User

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    # Register Blueprints
    from routes.auth import auth_bp
    from routes.admin import admin_bp
    from routes.lecturer import lecturer_bp
    from routes.student import student_bp

    app.register_blueprint(auth_bp, url_prefix='/auth')
    app.register_blueprint(admin_bp, url_prefix='/admin')
    app.register_blueprint(lecturer_bp, url_prefix='/lecturer')
    app.register_blueprint(student_bp, url_prefix='/student')

    # Root route redirect
    @app.route('/')
    def index():

        return render_template('index.html')

    return app

app = create_app()

if __name__ == '__main__':
    with app.app_context():
        # Ensures tables are created if running app.py directly
        db.create_all()
    app.run(debug=True)