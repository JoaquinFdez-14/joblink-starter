// api/controllers/ofertasController.js
import { db } from "../config/firebase.js";

export const getOfertas = async (req, res) => {
  try {
    const snap = await db.collection("ofertas").get();
    let result = snap.docs.map((doc) => ({ id: doc.id, ...doc.data() }));

    const { estado, empresaId, carrera, sede, tipo } = req.query;

    if (estado) result = result.filter((o) => o.estado === estado);
    if (empresaId) result = result.filter((o) => o.empresaId === empresaId);
    if (carrera)
      result = result.filter((o) =>
        (o.carrera_requerida || "").toLowerCase().includes(carrera.toLowerCase())
      );
    if (sede)
      result = result.filter((o) => (o.sede || "").toLowerCase().includes(sede.toLowerCase()));
    if (tipo)
      result = result.filter((o) => (o.tipo || "").toLowerCase().includes(tipo.toLowerCase()));

    res.json(result);
  } catch (err) {
    console.error("Error al obtener ofertas:", err);
    res.status(500).json({ error: "Error al obtener ofertas" });
  }
};

export const getOfertaById = async (req, res) => {
  try {
    const doc = await db.collection("ofertas").doc(req.params.id).get();
    if (!doc.exists) {
      return res.status(404).json({ error: "Oferta no encontrada" });
    }
    res.json({ id: doc.id, ...doc.data() });
  } catch (err) {
    console.error("Error al obtener oferta:", err);
    res.status(500).json({ error: "Error al obtener oferta" });
  }
};

export const createOferta = async (req, res) => {
  try {
    const { titulo, descripcion, carrera_requerida, sede, tipo, empresaId, estado } = req.body;

    if (!titulo || !empresaId) {
      return res.status(400).json({ error: "titulo y empresaId son obligatorios" });
    }

    const empresaDoc = await db.collection("usuarios").doc(empresaId).get();
    if (!empresaDoc.exists || empresaDoc.data().rol !== "empresa") {
      return res.status(400).json({ error: "empresaId no corresponde a una empresa válida" });
    }

    const nueva = {
      titulo,
      descripcion: descripcion || "",
      carrera_requerida: carrera_requerida || "",
      sede: sede || "",
      tipo: tipo || "",
      empresaId,
      estado: estado || "activa",
    };

    const ref = await db.collection("ofertas").add(nueva);
    res.status(201).json({ id: ref.id, ...nueva });
  } catch (err) {
    console.error("Error al crear oferta:", err);
    res.status(500).json({ error: "Error al crear oferta" });
  }
};

export const updateOferta = async (req, res) => {
  try {
    const ref = db.collection("ofertas").doc(req.params.id);
    const doc = await ref.get();
    if (!doc.exists) {
      return res.status(404).json({ error: "Oferta no encontrada" });
    }

    await ref.update(req.body);
    const updated = await ref.get();
    res.json({ id: updated.id, ...updated.data() });
  } catch (err) {
    console.error("Error al actualizar oferta:", err);
    res.status(500).json({ error: "Error al actualizar oferta" });
  }
};

export const deleteOferta = async (req, res) => {
  try {
    const ref = db.collection("ofertas").doc(req.params.id);
    const doc = await ref.get();
    if (!doc.exists) {
      return res.status(404).json({ error: "Oferta no encontrada" });
    }

    await ref.delete();
    res.json({ message: "Oferta eliminada" });
  } catch (err) {
    console.error("Error al eliminar oferta:", err);
    res.status(500).json({ error: "Error al eliminar oferta" });
  }
};
