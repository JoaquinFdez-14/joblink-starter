# JobLink Portal (Django)

## Requisitos
- Python 3.x
- pip install django requests

## Cómo correr
1. Instala dependencias:
   ```bash
   pip install django requests
   ```

2. Ejecuta migraciones iniciales de Django:
   ```bash
   python manage.py migrate
   ```

3. Levanta el servidor local:
   ```bash
   python manage.py runserver
   ```

4. Abre en el navegador:
   http://127.0.0.1:8000/

Esta vista intenta consultar la API Node.js en
http://localhost:8080/api/ofertas
y muestra cuántas ofertas vienen.

## Próximo paso
- Crear templates reales (listar ofertas con HTML)
- Formularios para postular
- Dashboards por rol
