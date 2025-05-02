from flask import Blueprint, render_template, request, redirect, url_for, flash

auth_bp = Blueprint('auth', __name__)

USERS = {
    'admin': 'adminpassword',
    'client': 'clientpassword'
}

@auth_bp.route('/', methods=['GET'])
def index():
    """Redireciona para a página de login."""
    return redirect(url_for('auth.login'))

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if username in USERS and USERS[username] == password:
            return redirect(url_for('campaign.campaign_config'))
        else:
            flash('Credenciais inválidas. Tente novamente.')
    return render_template('login.html')