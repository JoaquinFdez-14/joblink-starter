(function () {
  if (!window.firebase) {
    console.error("Firebase no está cargado");
    return;
  }
  async function postIdTokenToDjango(idToken) {
    const resp = await fetch("/auth/firebase-login/", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ idToken }),
    });
    const data = await resp.json().catch(() => ({}));
    if (!resp.ok) {
      throw new Error(data.detail || data.error || "Error de autenticación");
    }
    return data;
  }
  window.joblinkLogin = async function (email, password) {
    const cred = await firebase.auth().signInWithEmailAndPassword(email, password);
    // Ya no se exige verificación de correo
    const idToken = await cred.user.getIdToken(true);
    await postIdTokenToDjango(idToken);
    window.location.href = "/";
  };
})();