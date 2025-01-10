from flask import render_template, request, redirect, url_for, jsonify
from . import db
from .models import Usuario, Profesional, Cita, Disponibilidad
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

    @app.route('/disponibilidad/<profesional_id>') 
    def disponibilidad(profesional_id):
        """
        Obtiene las horas de un profesional, con opción de filtrarlas por turno.

        Args:
            profesional_id (int): ID del profesional cuyas horas se desean consultar.

        Query Parameters:
            turno (str, opcional): Turno de las horas a filtrar. Puede ser:
                - 'mañana': (<id>?turno=mañana) Filtra horas entre las 00:00 y 11:59.
                - 'tarde': (<id>?turno=tarde) Filtra horas entre las 12:00 y 17:59.
                - None: No se aplica filtro de turno, se incluyen todas las horas.

        Returns:
            Response: Objeto JSON con el siguiente formato:
                {
                    'horas': [
                        {'id': int, 'hora': str, 'estado': str},
                        ...
                    ]
                }
            Código de estado HTTP 200.
        """
        turno = request.args.get('turno')
        disponibilidad_obj = Disponibilidad.query.filter_by(profesional_id=profesional_id).all()
        horas = []
        ids= []
        estados = []
        
        for item in disponibilidad_obj:
            hora_actual = item.fecha_hora
            
            if turno == 'mañana' and hora_actual.hour < 12:
                ids.append(item.id)
                horas.append(hora_actual.strftime("%d/%m/%Y %H:%M:%S"))
                estados.append(item.estado)
            elif turno == 'tarde' and 12 <= hora_actual.hour < 18:
                ids.append(item.id)
                horas.append(hora_actual.strftime("%d/%m/%Y %H:%M:%S"))
                estados.append(item.estado)
            elif turno is None:  
                ids.append(item.id)
                horas.append(hora_actual.strftime("%d/%m/%Y %H:%M:%S"))
                estados.append(item.estado)
       
        id_hora_estado = []
        for id, hora, estado in zip(ids, horas, estados):
            id_hora_estado.append({'id': id, 'hora': hora, 'estado': estado})

        return jsonify({
            'horas': id_hora_estado
        }), 200
   
    @app.route('/hola_mundo')
    def index():
        fecha = datetime.now()
        fecha_formateada = fecha.strftime("%d/%m/%Y %H:%M:%S")
        mensaje = 'hola mundo, saapee!'
        return jsonify({'fecha': fecha_formateada, 'mensaje': mensaje}), 200
    