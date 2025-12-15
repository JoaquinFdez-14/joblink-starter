// api/controllers/postulacionesController.js
import { db } from "../config/firebase.js";
import { LOGROS } from "../entities/logro.js";

export const createPostulacion = async (req, res) => {
  try {
    const { ofertaId, estudianteId } = req.body;

    if (!ofertaId || !estudianteId) {
      return res.status(400).json({ error: "ofertaId y estudianteId son obligatorios" });
    }

    const ofertaDoc = await db.collection("ofertas").doc(ofertaId).get();
    if (!ofertaDoc.exists) {
      return res.status(404).json({ error: "Oferta no existe" });
    }

    const estDoc = await db.collection("usuarios").doc(estudianteId).get();
    if (!estDoc.exists || estDoc.data().rol !== "estudiante") {
      return res.status(400).json({ error: "estudianteId no es un estudiante válido" });
    }

    const dupSnap = await db
      .collection("postulaciones")
      .where("ofertaId", "==", ofertaId)
      .where("estudianteId", "==", estudianteId)
      .get();

    if (!dupSnap.empty) {
      return res.status(400).json({ error: "Ya estás postulando a esta oferta" });
    }

    const nueva = {
      ofertaId,
      estudianteId,
      fecha: new Date().toISOString(),
      estado: "postulado",
    };

    const ref = await db.collection("postulaciones").add(nueva);
    // --- Lógica de logros ---
    // Obtener postulaciones del usuario
    const postulacionesSnap = await db.collection("postulaciones").where("estudianteId", "==", estudianteId).get();
    const postulacionesCount = postulacionesSnap.size;
    const usuarioRef = db.collection("usuarios").doc(estudianteId);
    const usuarioDoc = await usuarioRef.get();
    let achievements = usuarioDoc.data().achievements || [];

    // Logro: primera postulación
    if (postulacionesCount === 1 && !achievements.includes("primer_postulacion")) {
      achievements.push("primer_postulacion");
    }
    // Logro: 5 postulaciones
    if (postulacionesCount === 5 && !achievements.includes("cinco_postulaciones")) {
      achievements.push("cinco_postulaciones");
    }
    if (achievements.length > (usuarioDoc.data().achievements || []).length) {
      await usuarioRef.update({ achievements });
    }

    res.status(201).json({ id: ref.id, ...nueva, newAchievements: achievements });
  } catch (err) {
    console.error("Error al crear postulación:", err);
    res.status(500).json({ error: "Error al crear postulación" });
  }
};

export const updatePostulacion = async (req, res) => {
  try {
    const { id } = req.params;
    const { estado } = req.body;
    if (!estado) {
      return res.status(400).json({ error: "estado es obligatorio" });
    }
    const ref = db.collection("postulaciones").doc(id);
    const doc = await ref.get();
    if (!doc.exists) {
      return res.status(404).json({ error: "Postulación no encontrada" });
    }
    await ref.update({ estado });
    const updated = await ref.get();
    res.json({ id: updated.id, ...updated.data() });
  } catch (err) {
    console.error("Error al actualizar postulación:", err);
    res.status(500).json({ error: "Error al actualizar postulación" });
  }
};

export const deletePostulacion = async (req, res) => {
  try {
    const { id } = req.params;
    const ref = db.collection("postulaciones").doc(id);
    const doc = await ref.get();
    if (!doc.exists) {
      return res.status(404).json({ error: "Postulación no encontrada" });
    }
    await ref.delete();
    res.json({ ok: true, id });
  } catch (err) {
    console.error("Error al eliminar postulación:", err);
    res.status(500).json({ error: "Error al eliminar postulación" });
  }
};

export const listPostulaciones = async (req, res) => {
  try {
    const { estudianteId } = req.query;

    let query = db.collection("postulaciones");
    if (estudianteId) {
      query = query.where("estudianteId", "==", estudianteId);
    }

    const snap = await query.get();
    const result = snap.docs.map((doc) => ({ id: doc.id, ...doc.data() }));

    res.json(result);
  } catch (err) {
    console.error("Error al obtener postulaciones:", err);
    res.status(500).json({ error: "Error al obtener postulaciones" });
  }
};
