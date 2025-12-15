// api/routes/postulaciones.js
import express from "express";
import { createPostulacion, listPostulaciones, updatePostulacion, deletePostulacion } from "../controllers/postulacionesController.js";
import { requireToken } from "../middleware/auth.js";

const router = express.Router();


router.post("/", requireToken, createPostulacion);
router.get("/", listPostulaciones);
router.put("/:id", requireToken, updatePostulacion);
router.delete("/:id", requireToken, deletePostulacion);

export default router;
