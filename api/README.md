# JobLink API (Node.js)

## Requisitos
- Node.js 18+
- npm

## Cómo correr
1. Instala dependencias:
   ```bash
   npm install
   ```
2. Levanta el servidor:
   ```bash
   npm run dev
   ```
3. Prueba en Postman / navegador:
   - GET http://localhost:8080/api/ofertas
   - POST http://localhost:8080/api/ofertas
   - POST http://localhost:8080/api/postulaciones
   - GET http://localhost:8080/api/postulaciones?estudianteId=alumno777

## Próximo paso
- Conectar Firestore (firebase-admin)
- Proteger rutas con Firebase Auth token
- Desplegar en Cloud Run
