from controllers.main_controller import main_bp
from controllers.auth_controller import auth_bp
from controllers.writer_controller import writer_bp
from controllers.admin_controller import admin_bp
from controllers.api_controller import api_bp

def register_blueprints(app):
    app.register_blueprint(main_bp)
    app.register_blueprint(auth_bp)
    app.register_blueprint(writer_bp)
    app.register_blueprint(admin_bp)
    app.register_blueprint(api_bp)
