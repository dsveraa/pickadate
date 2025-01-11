from ..models import Hora

class ListarHoras:
    def __init__(self, id, fecha_hora, estado):
        self.id = id
        self.fecha_hora = fecha_hora
        self.estado = estado

    def turno(self, turno):
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

def obtener_horas_filtradas(profesional_id, turno):
    
    disponibilidad_obj = Hora.query.filter_by(profesional_id=profesional_id).all()

    lista_horas = []
    for item in disponibilidad_obj:
        hora = ListarHoras(item.id, item.fecha_hora, item.estado)
        lista_horas.append(hora)

    horas_filtradas = []
    for hora in lista_horas:
        if hora.turno(turno):
            horas_filtradas.append(hora.to_dict())
    
    return horas_filtradas