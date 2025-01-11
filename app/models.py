from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from . import db

class DisponibilidadEstado:
    disponible = "disponible"
    ocupado = "ocupado"

class CitaEstado:
    confirmada = "confirmada"
    cancelada = "cancelada"
    pendiente = "pendiente"

class Especialidad(db.Model):
    __tablename__ = 'especialidades'

    id = Column(Integer, primary_key=True)
    nombre = Column(String(100), nullable=False, unique=True)

    profesionales = relationship("Profesional", back_populates="especialidad")

class Profesional(db.Model):
    __tablename__ = 'profesionales'

    id = Column(Integer, primary_key=True)
    nombre = Column(String(100), nullable=False)
    apellido = Column(String(100), nullable=False)
    especialidad_id = Column(Integer, ForeignKey('especialidades.id'), nullable=False)

    especialidad = relationship("Especialidad", back_populates="profesionales")
    horas = relationship("Hora", back_populates="profesional")
    citas = relationship("Cita", back_populates="profesional")

class Usuario(db.Model):
    __tablename__ = 'usuarios'

    id = Column(Integer, primary_key=True)
    nombre = Column(String(100), nullable=False)
    apellido = Column(String(100), nullable=False)
    rut = Column(String(12), nullable=False, unique=True)
    email = Column(String(150), nullable=False, unique=True)
    telefono = Column(String(15), nullable=False)

    citas = relationship("Cita", back_populates="usuario")

class Hora(db.Model):
    __tablename__ = 'horas'

    id = Column(Integer, primary_key=True)
    profesional_id = Column(Integer, ForeignKey('profesionales.id'), nullable=False)
    fecha_hora = Column(DateTime, nullable=False)
    estado = Column(String(50), default=DisponibilidadEstado.disponible, nullable=False)

    profesional = relationship("Profesional", back_populates="horas")
    cita = relationship("Cita", back_populates="hora", uselist=False)

class Cita(db.Model):
    __tablename__ = 'citas'

    id = Column(Integer, primary_key=True)
    usuario_id = Column(Integer, ForeignKey('usuarios.id'), nullable=False)
    profesional_id = Column(Integer, ForeignKey('profesionales.id'), nullable=False)
    fecha_hora_id = Column(Integer, ForeignKey('horas.id'), nullable=False)
    estado = Column(String(50), default=CitaEstado.pendiente, nullable=False)

    usuario = relationship("Usuario", back_populates="citas")
    profesional = relationship("Profesional", back_populates="citas")
    hora = relationship("Hora", back_populates="cita")
