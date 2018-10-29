###
# File that configures everything. Set macros here
###

# Database
DATABASE_NAME = 'CarteirinhaUFRJ'
DATABASE_URI = 'mongodb://127.0.0.1:27017/' + DATABASE_NAME

# Flask app
CSRF_SECRET_KEY = 'IUUIH@*HA#()RU)(A9102u'

# Views
LOGIN_VIEW = 'login'

# Models settings
CPF_LENGTH = 11
DRE_LENGTH = 9
MAX_FULLNAME_LENGTH = 50
MAX_COURSE_LENGTH = 50
DATE_FORMAT = '%d/%m/%Y'
EXPIRE_DAYS = 80