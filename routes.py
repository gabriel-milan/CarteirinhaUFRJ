#
#   Imports
#
import requests
from forms import *
from models import *
from protocol_utils import *
from datetime import datetime, timedelta
from werkzeug.security import generate_password_hash, check_password_hash
from flask import render_template, request, redirect, url_for, jsonify, flash
from flask_login import LoginManager, login_user, login_required, logout_user, current_user

#
#   Examples to create
#
print ("Creating users, this shouldn't take too long. In case it does, check if MongoDB service is up and running.")
check_user = User.objects(cpf="12627258796").first()
if not check_user:
    pacha = User( \
        cpf = "12627258796", \
        password = generate_password_hash("1234", method='sha256'), \
        full_name = "Bruno Pachá Moraes", \
        dre = "116046861", \
        course = "Engenharia da Computação e Informação", \
        birthdate = datetime.strptime("19/03/1998", "%d/%m/%Y"), \
        profile_pic_path = "/static/uploads/pacha.jpeg", \
        expire_date = datetime.strptime("31/12/2020", "%d/%m/%Y") \
    ).save()
check_user = User.objects(cpf="45049725810").first()
if not check_user:
    gazola = User( \
        cpf = "45049725810", \
        password = generate_password_hash("5077", method='sha256'), \
        full_name = "Gabriel Gazola Milan", \
        dre = "116034377", \
        course = "Engenharia Eletrônica e de Computação", \
        birthdate = datetime.strptime("12/04/1997", "%d/%m/%Y"), \
        profile_pic_path = "/static/uploads/gazola.jpeg", \
        expire_date = datetime.strptime("31/12/2019", "%d/%m/%Y") \
    ).save()

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
        if form.validate():
            check_user = User.objects(cpf=form.cpf.data).first()
            if check_user:
                if check_password_hash(check_user['password'], form.password.data):
                    login_user(check_user)
                    return redirect(url_for('carteirinha'))
                else:
                    response = generate_response({
                        'status' : 2,
                    })
                    return response
            else:
                response = generate_response({
                    'status' : 3,
                })
                return response
    return render_template('login.html', form=form)

# Route to login
@app.route('/login')
def login ():
    return redirect(url_for('homepage'))

# Route to generate the student card
@app.route('/carteirinha')
@login_required
def carteirinha():
    return render_template('carteirinha.html', user = current_user, birth = current_user.birthdate.strftime("%d/%m/%Y"), expire = current_user.expire_date.strftime("%d/%m/%Y"))

# Route to logout
@app.route('/logout', methods = ['GET'])
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(host = "0.0.0.0", debug = True)

# #
# #   Function to check protocol
# #
# def check_protocol ():
#     if (current_user['cpf']):
#         response = requests.post("http://127.0.0.1:5000/protocol", generate_request({"GET" : current_user['cpf'], "PASSWORD" : current_user['password']}))
#     else:
#         response = requests.post("http://127.0.0.1:5000/protocol", "")
#     return response

# # Route to protocol stuff
# @app.route('/protocol', methods=['POST'])
# def protocol():
#     if current_user.is_authenticated == True:
#         with open(current_user['profile_pic_path'], "rb") as imageFile:
#             f = imageFile.read()
#             b = bytearray(f)
#         response = generate_response({
#             'status' : 0,
#             'cpf' : check_user['cpf'],
#             'curso' : check_user['course'],
#             'dre' : check_user['dre'],
#             'nasc' : check_user['birthdate'],
#             'tamanho' : len(form.password.data),
#             'nome' : check_user['full_name'],
#             'foto' : b
#         })
#     else:
#         response = generate_response({
#             'status' : 1,
#         })
#     return response

# # Route to the main register page
# @app.route('/register', methods = ['GET', 'POST'])
# def register():
#     form = RegistrationForm()
#     if request.method == 'POST':
#         if True:#form.validate():
#             existing_user = User.objects(cpf=form.cpf.data).first()
#             if existing_user is None:
#                 if (form.password.data == form.password_confirmation.data):
#                     hashpass = generate_password_hash(form.password.data, method='sha256')
#                     pic_path = 'static/uploads/' + form.cpf.data + '.png'
#                     print (form.profile_pic)
#                     print (type(form.profile_pic))
#                     form.profile_pic.data.save(pic_path)
#                     new_user = User( \
#                         cpf = form.cpf.data, \
#                         password = hashpass, \
#                         full_name = form.full_name.data, \
#                         dre = form.dre.data, \
#                         course = form.course.data, \
#                         birthdate = form.birthdate.data, \
#                         profile_pic_path = pic_path, \
#                         expire_date = datetime.strftime(datetime.now() + timedelta(days = EXPIRE_DAYS), DATE_FORMAT) \
#                     )
#                     new_user.save()
#                     login_user(new_user)
#                     return redirect(url_for('carteirinha'))
#                 else:
#                     flash('As senhas não conferem!')
#                     # raise InvalidUsage('As senhas não conferem!', status_code = 400)
#             else:
#                 flash('Usuário já cadastrado!')
#                 # raise InvalidUsage('O usuário já existe!', status_code = 400)
#         else:
#             flash('Formulário não foi validado com sucesso :(')
#             # raise InvalidUsage('Formulário não validado, preencha novamente!', status_code = 400)
#     return render_template('register.html', form = form)