// api/entities/logro.js
export const LOGROS = [
  {
    id: "primer_postulacion",
    nombre: "Primera postulación",
    descripcion: "Enviaste tu primera postulación.",
    icono: "\uD83E\uDD47", // 🥇
    condicion: "postulaciones >= 1"
  },
  {
    id: "perfil_completo",
    nombre: "Perfil completo",
    descripcion: "Completaste todos los campos de tu perfil.",
    icono: "\uD83E\uDD48", // 🥈
    condicion: "perfil_completo == true"
  },
  {
    id: "postulacion_aceptada",
    nombre: "Postulación aceptada",
    descripcion: "Una de tus postulaciones fue aceptada.",
    icono: "\uD83E\uDD49", // 🥉
    condicion: "postulacion_aceptada == true"
  },
  {
    id: "cinco_postulaciones",
    nombre: "5 postulaciones enviadas",
    descripcion: "Enviaste 5 postulaciones.",
    icono: "\uD83D\uDD25", // 🔥
    condicion: "postulaciones >= 5"
  }
];
