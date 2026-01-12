from dataclasses import dataclass
from datetime import date, datetime
from typing import Optional


@dataclass
class Event:
    """
    Representa un evento del calendario.
    Puede ser puntual (un solo día) o de varios días (rango).
    """
    titulo: str
    descripcion: str
    categoria: str
    fecha_inicio: date
    fecha_fin: Optional[date] = None
    hora_inicio: Optional[str] = None  # "HH:MM"
    hora_fin: Optional[str] = None     # "HH:MM"

    @property
    def es_rango(self) -> bool:
        """True si el evento ocupa más de un día."""
        return self.fecha_fin is not None and self.fecha_fin > self.fecha_inicio

    @classmethod
    def desde_dict(cls, data: dict) -> "Event":
        """
        Crea un Event desde un diccionario y valida:
        - Campos obligatorios
        - Formato de fechas (YYYY-MM-DD)
        - Rango de fechas coherente
        """

        # 1) Campos obligatorios
        campos_obligatorios = ["titulo", "descripcion", "categoria", "fecha_inicio"]
        for campo in campos_obligatorios:
            if campo not in data or not data[campo]:
                raise ValueError(f"Falta el campo obligatorio: {campo}")

        # 2) fecha_inicio
        try:
            fecha_inicio = _parse_fecha(data["fecha_inicio"])
        except ValueError:
            raise ValueError(f"Formato de fecha incorrecto en fecha_inicio: {data['fecha_inicio']}")

        # 3) fecha_fin (opcional)
        fecha_fin = None
        if data.get("fecha_fin"):
            try:
                fecha_fin = _parse_fecha(data["fecha_fin"])
            except ValueError:
                raise ValueError(f"Formato de fecha incorrecto en fecha_fin: {data['fecha_fin']}")

        # 4) fecha_fin >= fecha_inicio (si existe)
        if fecha_fin and fecha_fin < fecha_inicio:
            raise ValueError("fecha_fin no puede ser anterior a fecha_inicio")

        return cls(
            titulo=data["titulo"],
            descripcion=data["descripcion"],
            categoria=data["categoria"],
            fecha_inicio=fecha_inicio,
            fecha_fin=fecha_fin,
            hora_inicio=data.get("hora_inicio"),
            hora_fin=data.get("hora_fin"),
        )


def _parse_fecha(valor) -> date:
    """
    Función auxiliar:
    - Si viene string 'YYYY-MM-DD' → lo parsea.
    - Si viene objeto date/datetime → lo adapta.
    """
    if isinstance(valor, date) and not isinstance(valor, datetime):
        return valor
    if isinstance(valor, datetime):
        return valor.date()
    if isinstance(valor, str):
        return datetime.strptime(valor, "%Y-%m-%d").date()
    raise ValueError(f"No se reconoce el tipo de fecha: {valor!r}")
