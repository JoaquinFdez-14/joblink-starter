// api/routes/api.js
import express from "express";
import { db } from "../config/firebase.js";

const router = express.Router();

// Endpoint de prueba de Firestore
router.get("/test-firestore", async (req, res) => {
  try {
    const snap = await db.collection("test").add({ createdAt: Date.now() });
    res.json({ ok: true, id: snap.id });
  } catch (e) {
    res.status(500).json({ ok: false, error: e.message });
  }
});

export default router;
