from flask import Blueprint, render_template, request, redirect, url_for, session, flash
from services.auth_service import auth_service
from services.notification_service import notification_service

auth_bp = Blueprint('auth', __name__)


@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        confirm_password = request.form['confirm_password']

        if password != confirm_password:
            flash('Паролите не съвпадат!', 'error')
            return render_template('register.html')

        user = auth_service.register(email, password)
        if user:
            notification_service.notify(user, "registration", None)
            flash('Регистрацията е успешна! Моля, влезте в акаунта си.', 'success')
            return redirect(url_for('auth.login'))
        else:
            flash('Потребител с този имейл вече съществува!', 'error')

    return render_template('register.html')


@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        user = auth_service.login(email, password)
        if user:
            session['user_id'] = user.id
            flash(f'Добре дошли, {email}!', 'success')
            return redirect(url_for('index'))
        else:
            flash('Грешен имейл или парола!', 'error')

    return render_template('login.html')


@auth_bp.route('/logout')
def logout():
    session.pop('user_id', None)
    flash('Излязохте успешно от акаунта си.', 'info')
    return redirect(url_for('index'))