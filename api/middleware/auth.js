(function () {
  if (!window.firebase) {
    console.error("Firebase no está cargado");
    return;
  }

  window.firebaseAuth = {
    async login(email, password) {
      try {
        const cred = await firebase
          .auth()
          .signInWithEmailAndPassword(email, password);

        if (!cred.user.emailVerified) {
          throw new Error("Debes verificar tu correo antes de ingresar.");
        }

        // 🔑 ESTE es el token correcto (ID TOKEN)
        const idToken = await cred.user.getIdToken(true);

        // Enviar token a Django
        const resp = await fetch("/auth/firebase-login/", {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({ idToken }),
        });

        const data = await resp.json();

        if (!resp.ok) {
          throw new Error(data.detail || data.error || "Error de autenticación");
        }

        // Login OK → recargar
        window.location.href = "/";
      } catch (err) {
        console.error("Login error:", err);
        alert(err.message || "Error al iniciar sesión");
      }
    },

    async logout() {
      await firebase.auth().signOut();
      window.location.href = "/logout/";
    },
  };
})();
