from flask import Flask, render_template, session, redirect, url_for
from controllers.auth_controller import auth_bp
from controllers.catalog_controller import catalog_bp
from controllers.cart_controller import cart_bp
from controllers.admin_controller import admin_bp

app = Flask(__name__)
app.secret_key = 'shoestore-secret-key-2024'


app.register_blueprint(auth_bp)
app.register_blueprint(catalog_bp)
app.register_blueprint(cart_bp)
app.register_blueprint(admin_bp)


@app.route('/')
def index():
    return render_template('index.html')


@app.context_processor
def inject_user():
    from services.auth_service import auth_service
    from services.notification_service import notification_service

    user = None
    notifications = []
    unread_count = 0

    if 'user_id' in session:
        user = auth_service.get_user_by_id(session['user_id'])
        if user:
            notifications = notification_service.get_user_notifications(user.id)
            unread_count = notification_service.get_unread_count(user.id)

    return dict(
        current_user=user,
        user_notifications=notifications[:5],
        unread_notifications_count=unread_count
    )


if __name__ == '__main__':
    app.run(debug=True)