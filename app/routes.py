from flask import render_template, request, redirect, url_for
from . import db
from .models import Usuario, Profesional, Cita
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from colorama import Fore, Style
from pytz import timezone, UTC
import inspect
import random
import pytz
from flask_cors import CORS


colors = [Fore.CYAN, Fore.GREEN]
last_color = None

def printn(message):
    global last_color
    frame = inspect.currentframe()
    info = inspect.getframeinfo(frame.f_back)
    new_color = random.choice([color for color in colors if color != last_color])
    last_color = new_color
    print(f"{new_color}[{info.lineno - 1}] {message}{Style.RESET_ALL}")

def process_datetime(client_timezone, datetime_obj):
    client_tz = pytz.timezone(client_timezone)
    client_datetime_tz = client_tz.localize(datetime_obj)
    client_datetime_utc = client_datetime_tz.astimezone(pytz.utc)   
    client_datetime_local = client_datetime_utc.astimezone(client_tz)
    date_local=client_datetime_local.isoformat()
    utc_iso_format = client_datetime_utc.isoformat()
    return date_local, utc_iso_format

def register_routes(app):
    CORS(app)

    @app.route('/hola_mundo')
    def index():
        printn("hola mundo, saapeee!")
        return "hola mundo, saapeee!"
   