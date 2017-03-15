# -*- coding: utf-8 -*-

from flask import Flask
from config import init_db

app = Flask(__name__)



@app.route('/')
def index():
    return 'Nikka/ app'


if __name__ == '__main__':
    init_db()

from app import views