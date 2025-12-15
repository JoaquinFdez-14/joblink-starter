import { initializeApp } from "https://www.gstatic.com/firebasejs/9.0.0/firebase-app.js";
import { getAuth } from "https://www.gstatic.com/firebasejs/9.0.0/firebase-auth.js";
import { getFirestore } from "https://www.gstatic.com/firebasejs/9.0.0/firebase-firestore.js";

const firebaseConfig = {
  apiKey: "AIzaSyD2C_YRvv3aerFVMg_XVMxxgn_IAEhiX4w",
  authDomain: "joblink-f0720.firebaseapp.com",
  projectId: "joblink-f0720",
  storageBucket: "joblink-f0720.firebasestorage.app",
  messagingSenderId: "546860779144",
  appId: "1:546860779144:web:282fb7844f139f0778813d",
  measurementId: "G-SQ1RSCLDLG"
};

const app = initializeApp(firebaseConfig);

const auth = getAuth(app);
const db = getFirestore(app);

export { auth, db };
