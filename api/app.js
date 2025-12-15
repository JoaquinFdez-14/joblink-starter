// api/app.js
import express from "express";
import cors from "cors";


import ofertasRouter from "./routes/ofertas.js";
import usuariosRouter from "./routes/usuarios.js";
import postulacionesRouter from "./routes/postulaciones.js";
import apiRouter from "./routes/api.js";

const app = express();
app.use(cors());
app.use(express.json());

app.get("/api/status", (req, res) => {
  res.json({ ok: true, mensaje: "API JobLink funcionando" });
});


app.use("/api/ofertas", ofertasRouter);
app.use("/api/usuarios", usuariosRouter);
app.use("/api/postulaciones", postulacionesRouter);
app.use("/api", apiRouter);

export default app;
