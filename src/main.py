from pathlib import Path
from src.reader_json import cargar_eventos_desde_json
from src.reader_excel import cargar_eventos_desde_excel


def main():
    base_path = Path(__file__).parent.parent
    json_path = base_path / "data" / "eventos.json"
    excel_path = base_path / "data" / "eventos.xlsx"

    # 1) Probar JSON
    try:
        eventos_json = cargar_eventos_desde_json(str(json_path))
        print("✅ Eventos cargados desde JSON:\n")
        for ev in eventos_json:
            rango = f"{ev.fecha_inicio} -> {ev.fecha_fin}" if ev.fecha_fin else str(ev.fecha_inicio)
            print(f"- {ev.titulo} ({rango}) [{ev.categoria}]")
    except Exception as e:
        print("❌ Error al cargar desde JSON:")
        print(e)

    print("\n" + "-" * 50 + "\n")

    # 2) Probar Excel
    try:
        eventos_excel = cargar_eventos_desde_excel(str(excel_path))
        print("✅ Eventos cargados desde Excel:\n")
        for ev in eventos_excel:
            rango = f"{ev.fecha_inicio} -> {ev.fecha_fin}" if ev.fecha_fin else str(ev.fecha_inicio)
            print(f"- {ev.titulo} ({rango}) [{ev.categoria}]")
    except Exception as e:
        print("❌ Error al cargar desde Excel:")
        print(e)


if __name__ == "__main__":
    main()
