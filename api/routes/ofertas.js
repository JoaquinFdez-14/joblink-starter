// api/routes/ofertas.js
import express from "express";
import {
  getOfertas,
  getOfertaById,
  createOferta,
  updateOferta,
  deleteOferta,
} from "../controllers/ofertasController.js";
import { requireToken } from "../middleware/auth.js";

const router = express.Router();

router.get("/", getOfertas);
router.get("/:id", getOfertaById);
router.post("/", requireToken, createOferta);
router.put("/:id", requireToken, updateOferta);
router.delete("/:id", requireToken, deleteOferta);

export default router;
