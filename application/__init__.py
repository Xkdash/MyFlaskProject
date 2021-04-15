from flask import Flask

def create_app():
    app = Flask(__name__)
    with app.app_context():
        app.secret_key="abc"
        from application.home import home_bp
        from application.hash_it.hash_it import hashit_bp
        from application.otp.otp_gen import otp_bp
        from application.hash_invert.hash_invert import invert_bp
        from application.vt_lookup.vt_lookup import vt_bp
        from application.treasure_hunt.hunt import hunt_bp
        # Register Blueprints
        app.register_blueprint(home_bp)
        app.register_blueprint(hashit_bp)
        app.register_blueprint(otp_bp)
        app.register_blueprint(invert_bp)
        app.register_blueprint(vt_bp)
        app.register_blueprint(hunt_bp,url_prefix="/treasure_hunt")
    return app
