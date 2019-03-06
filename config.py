import os

DATABASE_URL = os.getenv('DATABASE_URL')
SECRET = os.getenv('SECRET', 'secret here')
DOMAIN = os.getenv('DOMAIN')
