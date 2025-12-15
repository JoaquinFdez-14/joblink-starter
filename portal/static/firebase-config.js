// Import the functions you need from the SDKs you need
import { initializeApp } from "firebase/app";
import { getAnalytics } from "firebase/analytics";
// TODO: Add SDKs for Firebase products that you want to use
// https://firebase.google.com/docs/web/setup#available-libraries

// Your web app's Firebase configuration
// For Firebase JS SDK v7.20.0 and later, measurementId is optional
const firebaseConfig = {
  apiKey: "AIzaSyD2C_YRvv3aerFVMg_XVMxxgn_IAEhiX4w",
  authDomain: "joblink-f0720.firebaseapp.com",
  projectId: "joblink-f0720",
  storageBucket: "joblink-f0720.appspot.com", // CORREGIDO
  messagingSenderId: "546860779144",
  appId: "1:546860779144:web:282fb7844f139f0778813d",
  measurementId: "G-SQ1RSCLDLG"
};

// Initialize Firebase
const app = initializeApp(firebaseConfig);
const analytics = getAnalytics(app);

// Export app and analytics for use in other modules
export { app, analytics };
