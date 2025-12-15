
// api/server.js
import 'dotenv/config';
import app from "./app.js";
import { AUTH_TOKEN } from "./middleware/auth.js";

const PORT = process.env.PORT || 8080;
app.listen(PORT, () => {
  console.log(`✅ API JobLink en http://localhost:${PORT}`);
  console.log(`   Usa x-auth-token: ${AUTH_TOKEN} para POST/PUT/DELETE`);
});
