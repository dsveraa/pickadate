from flask import render_template, request, redirect, url_for, jsonify
from . import db
from .models import Usuario, Profesional, Cita, Hora
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

class ListarHoras:
    def __init__(self, id, fecha_hora, estado):
        self.id = id
        self.fecha_hora = fecha_hora
        self.estado = estado

    def es_turno(self, turno):
        if turno == 'mañana':
            return self.fecha_hora.hour < 12
        elif turno == 'tarde':
            return 12 <= self.fecha_hora.hour < 18
        return True

    def to_dict(self):
        return {
            'id': self.id,
            'hora': self.fecha_hora.strftime("%d/%m/%Y %H:%M:%S"),
            'estado': self.estado
        }

def register_routes(app):
    CORS(app)

    @app.route('/disponibilidad/<profesional_id>')
    def disponibilidad(profesional_id):        
        turno = request.args.get('turno')
        disponibilidad_obj = Hora.query.filter_by(profesional_id=profesional_id).all()

        lista_horas = []
        for item in disponibilidad_obj:
            hora = ListarHoras(item.id, item.fecha_hora, item.estado)
            lista_horas.append(hora)

        horas_filtradas = []
        for hora in lista_horas:
            if hora.es_turno(turno):
                horas_filtradas.append(hora.to_dict())

        return jsonify({'horas': horas_filtradas}), 200

   
    @app.route('/hola_mundo')
    def index():
        fecha = datetime.now()
        fecha_formateada = fecha.strftime("%d/%m/%Y %H:%M:%S")
        mensaje = 'hola mundo, saapee!'
        return jsonify({'fecha': fecha_formateada, 'mensaje': mensaje}), 200
    