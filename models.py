#
#   Imports
#
from app import *
from flask_login import UserMixin
from flask_mongoengine import Document
from mongoengine import ReferenceField, ListField
from wtforms import StringField, BooleanField

#
#   User model
#
class User(UserMixin, db.Document):
    meta = {
        'collection': 'User',
        'allow_inheritance': True
    }
    dre = db.StringField(max_length = DRE_LENGTH, required = True)
    cpf = db.StringField(max_length = CPF_LENGTH, required = True)
    password = db.StringField(required = True)
    full_name = db.StringField(max_length = MAX_FULLNAME_LENGTH, required = True)
    course = db.StringField(max_length = MAX_COURSE_LENGTH, required = True)
    birthdate = db.DateTimeField(required = True)
    profile_pic_path = db.StringField(required = True)
    expire_date = db.DateTimeField(required = True)