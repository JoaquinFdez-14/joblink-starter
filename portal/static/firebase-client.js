// Cliente ligero que usa la API compat (cargada desde CDN) y expone funciones simples
(function () {
  if (!window.firebase) {
    console.warn('Firebase SDK no cargado (asegúrate de incluir los scripts CDN antes).');
    return;
  }

  // Debes configurar tu proyecto en `static/firebase.js` (ya incluido para módulos)
  // Aquí simplemente usamos window.firebase global (compat layer)

  window.firebaseAuth = {
    async register(email, password) {
      try {
        const userCredential = await firebase.auth().createUserWithEmailAndPassword(email, password);
        await userCredential.user.sendEmailVerification();
        return userCredential.user;
      } catch (err) {
        console.error('Firebase register error', err);
        // Mostrar mensajes más amigables según el código de error
        if (err && err.code === 'auth/configuration-not-found') {
          throw new Error('Error de configuración de Firebase: activa el método Email/Password en Firebase Console → Authentication → Sign-in method.');
        }
        if (err && err.code === 'auth/email-already-in-use') {
          throw new Error('El correo ya está en uso. Intenta iniciar sesión o usar otro correo.');
        }
        throw err;
      }
    },

    async login(email, password) {
      try {
        const userCredential = await firebase.auth().signInWithEmailAndPassword(email, password);
        if (!userCredential.user.emailVerified) {
          throw new Error('Por favor verifica tu correo antes de acceder.');
        }
        const idToken = await userCredential.user.getIdToken();
        await fetch('/auth/firebase-login/', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ idToken })
        });
        return userCredential.user;
      } catch (err) {
        console.error('Firebase login error', err);
        if (err && err.code === 'auth/configuration-not-found') {
          throw new Error('Error de configuración de Firebase: activa Email/Password en Firebase Console → Authentication → Sign-in method.');
        }
        if (err && err.code === 'auth/user-not-found') {
          throw new Error('Usuario no encontrado. Revisa el correo o regístrate primero.');
        }
        if (err && err.code === 'auth/wrong-password') {
          throw new Error('Contraseña incorrecta.');
        }
        throw err;
      }
    },

    async resetPassword(email) {
      return firebase.auth().sendPasswordResetEmail(email);
    },

    async logout() {
      await firebase.auth().signOut();
      return fetch('/logout/');
    }
  };
})();
