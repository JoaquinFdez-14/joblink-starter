// api/config/firebase.js

import admin from "firebase-admin";
import { getFirestore } from "firebase-admin/firestore";

// Cargar el serviceAccountKey.json usando import assertion

import fs from "fs/promises";
import path from "node:path";

let serviceAccount = {};
const credPath = process.env.GOOGLE_APPLICATION_CREDENTIALS || "./serviceAccountKey.json";
const absPath = path.isAbsolute(credPath) ? credPath : path.resolve(process.cwd(), credPath);

try {
  const jsonData = await fs.readFile(absPath, "utf-8");
  serviceAccount = JSON.parse(jsonData);
} catch (err) {
  throw new Error("No se pudo cargar el serviceAccountKey.json: " + err.message);
}

if (!admin.apps.length) {
  admin.initializeApp({
    credential: admin.credential.cert(serviceAccount),
  });
}

const db = getFirestore();
export { db, admin };
