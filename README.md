# Contador de Beneficios para Hijas

Aplicación web en Flask para registrar tareas domésticas y convertirlas en minutos de uso de celular para cada hija.

## Características

- Dashboard con resumen general:
  - Minutos acumulados por hija.
  - Cantidad de tareas realizadas.
  - Últimos registros cargados.
  - Gráfico comparativo.
- ABM de hijas (alta, edición, eliminación).
- ABM de actividades predefinidas.
- Registro de tarea realizada con:
  - hija,
  - actividad,
  - fecha/hora,
  - observación opcional.
- Historial con filtros por hija, actividad y rango de fechas.
- Eliminación de registros erróneos.
- Reportes con Chart.js:
  - minutos por hija,
  - actividades más frecuentes,
  - resumen de últimos 7 días.

## Requisitos

- Python 3.10+
- pip

## Instalación

1. Clonar el repositorio o ubicarse en la carpeta del proyecto.
2. Crear entorno virtual:

```bash
python -m venv .venv
```

3. Activar entorno virtual:

- Linux/macOS:

```bash
source .venv/bin/activate
```

- Windows (PowerShell):

```powershell
.venv\Scripts\Activate.ps1
```

4. Instalar dependencias:

```bash
pip install -r requirements.txt
```

## Inicializar base de datos (con datos de ejemplo)

```bash
flask --app app.py init-db
```

Este comando:
- crea tablas,
- carga 2 hijas de ejemplo,
- carga actividades predefinidas.

## Ejecutar

### Opción 1

```bash
python app.py
```

### Opción 2

```bash
flask --app app.py run
```

Abrir en el navegador: `http://127.0.0.1:5000`.

## Estructura del proyecto

```text
Codigo_IA/
├── app/
│   ├── routes/
│   │   ├── activities.py
│   │   ├── children.py
│   │   ├── dashboard.py
│   │   ├── logs.py
│   │   └── reports.py
│   ├── static/css/styles.css
│   ├── templates/
│   │   ├── activities/
│   │   ├── children/
│   │   ├── logs/
│   │   ├── reports/
│   │   ├── errors/
│   │   ├── base.html
│   │   └── dashboard.html
│   ├── __init__.py
│   ├── config.py
│   ├── extensions.py
│   ├── models.py
│   └── services.py
├── instance/
├── .gitignore
├── app.py
├── requirements.txt
└── README.md
```

## Decisiones técnicas

- Se usa `Flask-SQLAlchemy` con SQLite para mantener simplicidad y portabilidad local.
- Se usa factory pattern (`create_app`) para mejor organización.
- Los minutos otorgados se guardan en `reward_minutes_snapshot` al registrar la actividad para preservar histórico.
- Interfaz con Semantic UI + jQuery + Chart.js por CDN, sin frontend complejo.

## Mejoras futuras

- Agregar autenticación de usuarios.
- Incorporar paginación en historial.
- Exportar reportes en CSV/PDF.
- Añadir pruebas automáticas.
