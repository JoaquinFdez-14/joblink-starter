// api/routes/usuarios.js
import express from "express";
import {
  upsertUsuario,
  listUsuarios,
  getUsuario,
  getEmpleabilidad,
} from "../controllers/usuariosController.js";
import { requireToken } from "../middleware/auth.js";

const router = express.Router();


router.post("/", requireToken, upsertUsuario);
router.get("/", listUsuarios);
router.get("/:uid", getUsuario);
router.get("/:uid/empleabilidad", getEmpleabilidad);

export default router;
