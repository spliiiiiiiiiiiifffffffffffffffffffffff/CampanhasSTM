from flask import Blueprint, render_template, request, redirect, url_for, flash, session, current_app
import os
import json

auth_bp = Blueprint('auth', __name__)

def get_logins_file():
    return os.path.join(current_app.root_path, 'data', 'Logins.json')

@auth_bp.route('/', methods=['GET'])
def index():
    """Redireciona para a página de login."""
    return redirect(url_for('auth.login'))

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        logins_file = get_logins_file()
        if os.path.exists(logins_file):
            with open(logins_file, 'r') as file:
                users = json.load(file)
        else:
            users = []

        user = next((u for u in users if u['username'] == username and u['password'] == password), None)
        if user:
            session['username'] = user['username']
            session['tipo'] = user['tipo']
            return redirect(url_for('campaign.campaign_config'))
        else:
            flash('Credenciais inválidas. Tente novamente.')
    return render_template('login.html')