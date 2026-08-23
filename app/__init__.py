from flask import Flask, render_template

from config import Config
from .extensions import csrf, db, login_manager, migrate


def create_app(config_object=Config):
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_object(config_object)

    db.init_app(app)
    login_manager.init_app(app)
    migrate.init_app(app, db)
    csrf.init_app(app)

    from .models import User
    from .routes.admin import admin_bp
    from .routes.auth import auth_bp
    from .routes.cart import cart_bp
    from .routes.orders import orders_bp
    from .routes.shop import shop_bp

    app.register_blueprint(auth_bp)
    app.register_blueprint(shop_bp)
    app.register_blueprint(cart_bp)
    app.register_blueprint(orders_bp)
    app.register_blueprint(admin_bp)

    @login_manager.user_loader
    def load_user(user_id):
        return db.session.get(User, int(user_id))

    @app.errorhandler(403)
    def forbidden(_error):
        return render_template("errors/403.html"), 403

    @app.errorhandler(404)
    def not_found(_error):
        return render_template("errors/404.html"), 404

    @app.context_processor
    def global_context():
        from flask_login import current_user
        from .models import Cart

        cart_count = 0
        if current_user.is_authenticated:
            cart = Cart.query.filter_by(user_id=current_user.id, active=True).first()
            if cart:
                cart_count = sum(item.quantity for item in cart.items)
        return {"cart_count": cart_count}

    from .cli import register_commands

    register_commands(app)
    return app


