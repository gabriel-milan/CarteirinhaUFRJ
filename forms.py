#
#   Imports
#
from settings import *
from flask_wtf import FlaskForm
from wtforms.validators import Email, Length, InputRequired
from wtforms.ext.dateutil.fields import DateTimeField
from wtforms import StringField, PasswordField, FileField

#
#   Login form
#
class LoginForm (FlaskForm):
    cpf = StringField('cpf', validators=[InputRequired(), Length(max = CPF_LENGTH)])
    password = PasswordField('password', validators=[InputRequired()])

#
#   Register form
#
class RegistrationForm (FlaskForm):
    dre = StringField('dre', validators=[Length(DRE_LENGTH), InputRequired()])
    cpf = StringField('cpf', validators=[Length(CPF_LENGTH), InputRequired()])
    password = PasswordField('password', validators=[InputRequired()])
    password_confirmation = PasswordField('password', validators=[InputRequired()])
    full_name = StringField('full_name', validators=[Length(max = MAX_FULLNAME_LENGTH), InputRequired()])
    course = StringField('course', validators=[Length(max = MAX_COURSE_LENGTH), InputRequired()])
    birthdate = DateTimeField('birthdate', validators=[InputRequired()])
    profile_pic = FileField(validators=[InputRequired()])
