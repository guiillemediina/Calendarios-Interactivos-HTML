from dataclasses import dataclass
from datetime import datetime, date
from typing import List, Optional

@dataclass
class Event:
    "Representa un evento del calendario. Puede ser puntual de un dia o de varios dias"
    titulo:str
    descripcion:Optional[str]
    categoria:Optional[str]
    fecha_inicio:date
    fecha_fin:Optional[date] = None
    hora_inicio:Optional[datetime] = None
    hora_fin:Optional[datetime] = None

@property
def variosDias(self) -> bool:
    "Indica si el evento dura varios dias"
    return self.fecha_fin is not None and self.fecha_fin > self.fecha_inicio

@classmethod
def desde_dict(cls, data: dict) -> 'Event':
    """
    Crea una instancia de Event a partir de un diccionario
    - Campos obligatorios
    - Formato de fechas
    - Rango de fechas coherente
    """

    required_fields = ["titulo", "descripcion", "categoria", "fecha_inicio"]
    for field in required_fields:
        if field not in data:
            raise ValueError(f"Falta el campo obligatorio: {field}")
        
    try:
        fecha_inicio = _parse_date(data["fecha_inicio"])
    except ValueError:
        raise ValueError("Formato de fecha_inicio incorrecto. Se espera 'YYYY-MM-DD'")
    
    fecha_fin = None
    if data.get("fecha_fin"):
        try:
            fecha_fin = _parse_date(data["fecha_fin"])
        except ValueError:
            raise ValueError("Formato de fecha_fin incorrecto. Se espera 'YYYY-MM-DD'")
        
        if fecha_fin < fecha_inicio:
            raise ValueError("fecha_fin no puede ser anterior a fecha_inicio")
        
        return cls(
            titulo=data["titulo"],
            descripcion=data.get("descripcion"),
            categoria=data.get("categoria"),
            fecha_inicio=fecha_inicio,
            fecha_fin=fecha_fin,
            hora_inicio=data.get("hora_inicio"),
            hora_fin=data.get("hora_fin")
        )

def _parse_date(value) -> date:
    """
    Funcion auxiliar:
    - Si viene string 'YYYY-MM-DD', lo convierte a date
    - Si viene objeto date/datetime, (excel), lo adapta
    """    

    if isinstance(value, date):
        return value
    if isinstance(value, datetime):
        return value.date()
    if isinstance(value, str):
        return datetime.strptime(value, "%Y-%m-%d").date()
    raise ValueError("Formato de fecha no reconocido")




