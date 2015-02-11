import os
basedir = os.path.abspath(os.path.dirname(__file__))

# database
SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'chinese-whispers.db')
SQLALCHEMY_MIGRATE_REPO = os.path.join(basedir, 'db_repository')

# email server
MAIL_SERVER = "smtp.googlemail.com"
MAIL_PORT = 465
MAIL_USE_TSL = False
MAIL_USE_SSL = True
MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')

ADMINS = ['chinese.whispers@gmail.com', 'fbkarsdorp@fastmail.nl']