import json
from typing import List
from .models import Event  # import relativo dentro de src


def cargar_eventos_desde_json(path: str) -> List[Event]:
    """
    Lee eventos desde un archivo JSON y devuelve una lista de objetos Event
    
    Estructura esperada del JSON:
    [
        {
            "titulo": "Evento 1",
            "descripcion": "Descripcion del evento 1",
            "categoria": "Categoria A",
            "fecha_inicio": "2024-07-01",
            "fecha_fin": "2024-07-03",
            "hora_inicio": "10:00",
            "hora_fin": "12:00"
        },
        ...
    ]
    """

    # 1) Intentar abrir el archivo
    try:
        with open(path, 'r', encoding='utf-8') as file:
            data = json.load(file)
    except FileNotFoundError:
        raise FileNotFoundError(f"No se encontró el archivo: {path}")
    except json.JSONDecodeError as e:
        raise ValueError(f"Error al parsear JSON: {e}")
    
    # 2) Validar que el JSON tenga una lista
    if not isinstance(data, list):
        raise ValueError("El JSON debe contener una lista de eventos")
    
    eventos: List[Event] = []
    errors: List[str] = []

    # 3) Convertir cada dict a Event usando Event.desde_dict
    for index, item in enumerate(data, start=1):
        try:
            evento = Event.desde_dict(item)
            eventos.append(evento)
        except ValueError as e:
            errors.append(f"Error en el evento índice {index}: {e}")

    # 4) Si hay errores, los juntamos y lanzamos una excepción clara
    if errors:
        error_messages = "\n".join(errors)
        raise ValueError(f"Se encontraron errores al cargar eventos:\n{error_messages}")

    return eventos
