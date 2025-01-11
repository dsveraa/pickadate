from flask import render_template, request, redirect, url_for, jsonify
from datetime import datetime
from flask_cors import CORS

from .utils.validaciones import validar_rut
from .utils.debugging import printn
from .services.horas_service import obtener_horas_filtradas

def register_routes(app):
    CORS(app)

    @app.route('/agendar', methods=["POST"])
    def agendar():
        rut_usuario = request.form["rut"]
        nombre = request.form["nombre"]
        
        if validar_rut(rut_usuario):
            status = 'success'
        else:
            status = 'failed'
            
        return jsonify({'rut': rut_usuario, 'nombre': nombre, 'status': status})

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
        horas_filtradas = obtener_horas_filtradas(profesional_id, turno)

        return jsonify({'horas': horas_filtradas}), 200
   
    @app.route('/hola_mundo')
    def index():
        fecha = datetime.now()
        fecha_formateada = fecha.strftime("%d/%m/%Y %H:%M:%S")
        mensaje = 'hola mundo, saapee!'
        return jsonify({'fecha': fecha_formateada, 'mensaje': mensaje}), 200
    