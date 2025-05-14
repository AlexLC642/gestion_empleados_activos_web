# config.py

import os

BASE_DIR = os.path.abspath(os.path.dirname(__file__))

class Config:
    SECRET_KEY = 'clave_secreta_super_segura_123'
    DATABASE = os.path.join(BASE_DIR, 'database', 'db.sqlite3')
