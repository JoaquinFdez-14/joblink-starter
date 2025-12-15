
# JobLink Proyecto Final

## Descripción General

JobLink es una plataforma web que conecta estudiantes y empresas para prácticas y empleos, usando una API Node.js con Firestore y un portal Django como frontend. Incluye autenticación, filtros, dashboards y recomendaciones personalizadas.

---

## Estructura del Proyecto

```
proyecto/
 ┣ portal/ (Django)
 ┃ ┣ manage.py
 ┃ ┣ core/
 ┃ ┣ templates/
 ┃ ┗ static/
 ┣ api/ (Node.js)
 ┃ ┣ server.js
 ┃ ┣ app.js
 ┃ ┣ config/
 ┃ ┣ controllers/
 ┃ ┣ routes/
 ┃ ┣ middleware/
 ┃ ┣ package.json
 ┃ ┗ .env.example
 ┗ firebase.json
```

---

## Instalación y Ejecución

### 1. Node API

1. Copia tu archivo `serviceAccountKey.json` en la carpeta `api/` (no lo subas al repo).
2. Crea un archivo `.env` en `api/` con:
   ```
   PORT=3001
   GOOGLE_APPLICATION_CREDENTIALS=./serviceAccountKey.json
   FIREBASE_PROJECT_ID=TU_PROJECT_ID
   ```
3. Instala dependencias:
   ```
   cd api
   npm install
   ```
4. Inicia la API:
   ```
   npm start
   ```
5. Prueba el endpoint de salud:
   - [http://localhost:3001/api/status](http://localhost:3001/api/status)

### 2. Django Portal

1. Instala dependencias:
   ```
   cd portal
   pip install -r requirements.txt
   ```
2. Ejecuta el servidor:
   ```
   python manage.py runserver
   ```
3. Accede a [http://localhost:8000/](http://localhost:8000/)

---

## Endpoints Principales (Node API)

- **Ofertas**
  - `GET /api/ofertas` — Listar ofertas (filtros: carrera, sede, tipo)
  - `GET /api/ofertas/:id` — Detalle de oferta
  - `POST /api/ofertas` — Crear oferta *(requiere x-auth-token)*
  - `PUT /api/ofertas/:id` — Editar oferta *(requiere x-auth-token)*
  - `DELETE /api/ofertas/:id` — Eliminar oferta *(requiere x-auth-token)*

- **Postulaciones**
  - `GET /api/postulaciones` — Listar postulaciones (filtro: estudianteId)
  - `POST /api/postulaciones` — Crear postulación *(requiere x-auth-token)*
  - `PUT /api/postulaciones/:id` — Cambiar estado *(requiere x-auth-token)*
  - `DELETE /api/postulaciones/:id` — Eliminar *(requiere x-auth-token)*

- **Usuarios**
  - `GET /api/usuarios` — Listar usuarios
  - `GET /api/usuarios/:uid` — Detalle usuario
  - `POST /api/usuarios` — Crear/actualizar usuario *(requiere x-auth-token)*

---

## Seguridad y Autenticación

- Todos los endpoints de modificación (POST, PUT, DELETE) requieren el header:
  ```
  x-auth-token: secreto123
  ```
  Puedes cambiar el valor en `.env` y en `settings.py` de Django.

---

## Flujo de la Aplicación

1. **Login:** El usuario ingresa UID, nombre y rol. Se guarda en sesión y se sincroniza con la API.
2. **Onboarding:** El estudiante completa sus preferencias (carrera, sede, intereses), que se sincronizan con la API.
3. **Ofertas:** Se listan todas las ofertas y se pueden filtrar. Se muestran recomendaciones según preferencias.
4. **Postulaciones:** El estudiante puede postular a ofertas. Puede ver el estado de sus postulaciones y el detalle de cada una.
5. **Panel Admin:** Permite ver y gestionar usuarios, ofertas y postulaciones.

---

## Evidencia para la entrega

- Captura de Firestore mostrando colecciones y documentos.
- Capturas de Postman probando:
  - Crear oferta
  - Listar ofertas
  - Crear postulación
  - Cambiar estado de postulación (PUT)
- Capturas del portal Django:
  - Listado de ofertas con filtros
  - Perfil y onboarding
  - Estado de postulaciones

---

## Notas finales

- No subas tu archivo `serviceAccountKey.json` ni la carpeta `node_modules` al repositorio o ZIP final.
- Incluye este README y .env.example para facilitar la revisión.
- Si tienes dudas, revisa los comentarios en el código y este documento.
