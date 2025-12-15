(function () {
  if (!window.firebase) {
    console.error("Firebase SDK compat no está cargado.");
    return;
  }
  const firebaseConfig = {
    apiKey: "AIzaSyD2C_YRvv3aerFVMg_XVMxxgn_IAEhiX4w",
    authDomain: "joblink-f0720.firebaseapp.com",
    projectId: "joblink-f0720",
    storageBucket: "joblink-f0720.appspot.com",
    messagingSenderId: "546860779144",
    appId: "1:546860779144:web:282fb7844f139f0778813d",
  };
  if (!firebase.apps.length) {
    firebase.initializeApp(firebaseConfig);
  }
})();