#
#   Imports
#
from forms import *
from models import *
from datetime import datetime, timedelta
from werkzeug.security import generate_password_hash, check_password_hash
from flask import render_template, request, redirect, url_for, jsonify, flash
from flask_login import LoginManager, login_user, login_required, logout_user, current_user

#
#   Login Manager
#
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = LOGIN_VIEW

@login_manager.user_loader
def load_user(user_id):
    user = User.objects(pk=user_id).first()
    return user

#
#   Exception class (from flask Docs, minor changes)
#
class InvalidUsage(Exception):
    status_code = 400

    def __init__(self, message, status_code=None, payload=None):
        Exception.__init__(self)
        self.message = message
        if status_code is not None:
            self.status_code = status_code
        self.payload = payload

    def to_dict(self):
        rv = dict(self.payload or ())
        rv['error_message'] = self.message
        rv['error_code'] = self.status_code
        return rv

#
#   Error pages
#
@app.errorhandler(InvalidUsage)
def unauthorized (error):
    response = jsonify(error.to_dict())
    response.status_code = error.status_code
    return render_template('error_page.html', error_code = error.status_code, error_message = error.message)

#
#   Routes
#

# Route to homepage
@app.route('/', methods = ['GET', 'POST'])
def homepage():
    if current_user.is_authenticated == True:
        return redirect(url_for('carteirinha'))
    form = LoginForm()
    if request.method == 'POST':
        # Parse stuff
        if form.validate():
            check_user = User.objects(cpf=form.cpf.data).first()
            if check_user:
                if check_password_hash(check_user['password'], form.password.data):
                    login_user(check_user)
                    return redirect(url_for('carteirinha'))
    return render_template('login.html', form=form)

# Route to login
@app.route('/login')
def login ():
    return redirect(url_for('homepage'))

# Route to the main register page
@app.route('/register', methods = ['GET', 'POST'])
def register():
    form = RegistrationForm()
    if request.method == 'POST':
        if True:#form.validate():
            existing_user = User.objects(cpf=form.cpf.data).first()
            if existing_user is None:
                if (form.password.data == form.password_confirmation.data):
                    hashpass = generate_password_hash(form.password.data, method='sha256')
                    pic_path = 'uploads/' + form.cpf.data + '.png'
                    print (form.profile_pic)
                    print (type(form.profile_pic))
                    form.profile_pic.data.save(pic_path)
                    new_user = User( \
                        cpf = form.cpf.data, \
                        password = hashpass, \
                        full_name = form.full_name.data, \
                        dre = form.dre.data, \
                        course = form.course.data, \
                        birthdate = form.birthdate.data, \
                        profile_pic_path = pic_path, \
                        expire_date = datetime.strftime(datetime.now() + timedelta(days = EXPIRE_DAYS), DATE_FORMAT) \
                    )
                    new_user.save()
                    login_user(new_user)
                    return redirect(url_for('carteirinha'))
                else:
                    flash('As senhas não conferem!')
                    # raise InvalidUsage('As senhas não conferem!', status_code = 400)
            else:
                flash('Usuário já cadastrado!')
                # raise InvalidUsage('O usuário já existe!', status_code = 400)
        else:
            flash('Formulário não foi validado com sucesso :(')
            # raise InvalidUsage('Formulário não validado, preencha novamente!', status_code = 400)
    return render_template('register.html', form = form)

# Route to generate the student card
@app.route('/carteirinha')
@login_required
def carteirinha():
    content = ""
    # Fazer empacotamento dos dados para enviar
    return render_template('carteirinha.html', content = content)

# Route to logout
@app.route('/logout', methods = ['GET'])
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(host = "0.0.0.0", debug = True)