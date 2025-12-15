// Endpoint: progreso de empleabilidad
export const getEmpleabilidad = async (req, res) => {
  try {
    const uid = req.params.uid;
    const doc = await db.collection("usuarios").doc(uid).get();
    if (!doc.exists) {
      return res.status(404).json({ error: "Usuario no encontrado" });
    }
    const user = doc.data();
    // 1. Perfil completo: +30%
    const camposPerfil = ["nombre", "rol", "carrera", "sede", "tipo_practica", "institucion", "intereses"];
    const perfilCompleto = camposPerfil.every((k) => user[k] && user[k] !== "");
    // 2. CV subido: +20%
    const cvSubido = !!user.cv_url;
    // 3. 3 postulaciones: +20%
    const postulacionesSnap = await db.collection("postulaciones").where("estudianteId", "==", uid).get();
    const tresPostulaciones = postulacionesSnap.size >= 3;
    // 4. Skills definidas: +30%
    const skillsDefinidas = Array.isArray(user.intereses) && user.intereses.length > 0;
    let porcentaje = 0;
    if (perfilCompleto) porcentaje += 30;
    if (cvSubido) porcentaje += 20;
    if (tresPostulaciones) porcentaje += 20;
    if (skillsDefinidas) porcentaje += 30;
    res.json({
      porcentaje,
      criterios: {
        perfil_completo: perfilCompleto,
        cv_subido: cvSubido,
        tres_postulaciones: tresPostulaciones,
        skills_definidas: skillsDefinidas
      }
    });
  } catch (err) {
    console.error("Error al calcular empleabilidad:", err);
    res.status(500).json({ error: "Error al calcular empleabilidad" });
  }
};
// api/controllers/usuariosController.js
import { db } from "../config/firebase.js";

export const upsertUsuario = async (req, res) => {
  try {
    const { uid, email, password } = req.body;

    if (!uid || !email || !password) {
      return res.status(400).json({ error: "uid, email y password son obligatorios" });
    }

    // Crear usuario en Firebase Auth si no existe
    let userRecord;
    try {
      userRecord = await (await import("../config/firebase.js")).admin.auth().getUser(uid);
    } catch (e) {
      // Si no existe, lo creamos
      userRecord = await (await import("../config/firebase.js")).admin.auth().createUser({
        uid,
        email,
        password
      });
    }

    // Build data object only with provided fields to avoid overwriting
    const allowed = ["nombre", "rol", "carrera", "sede", "tipo_practica", "institucion", "intereses"];
    const data = {};
    for (const key of allowed) {
      if (req.body[key] !== undefined) data[key] = req.body[key];
    }
    if (!data.rol) data.rol = req.body.rol || "estudiante";

    const ref = db.collection("usuarios").doc(uid);
    await ref.set(data, { merge: true });

    const doc = await ref.get();
    res.json({ uid: doc.id, ...doc.data() });
  } catch (err) {
    console.error("Error al crear/actualizar usuario:", err);
    res.status(500).json({ error: "Error al crear/actualizar usuario" });
  }
};

export const listUsuarios = async (req, res) => {
  try {
    const { rol } = req.query;

    let query = db.collection("usuarios");
    if (rol) {
      query = query.where("rol", "==", rol);
    }

    const snap = await query.get();
    const result = snap.docs.map((doc) => ({ uid: doc.id, ...doc.data() }));

    res.json(result);
  } catch (err) {
    console.error("Error al obtener usuarios:", err);
    res.status(500).json({ error: "Error al obtener usuarios" });
  }
};

export const getUsuario = async (req, res) => {
  try {
    const doc = await db.collection("usuarios").doc(req.params.uid).get();
    if (!doc.exists) {
      return res.status(404).json({ error: "Usuario no encontrado" });
    }
    res.json({ uid: doc.id, ...doc.data() });
  } catch (err) {
    console.error("Error al obtener usuario:", err);
    res.status(500).json({ error: "Error al obtener usuario" });
  }
};
