import * as dotenv from "dotenv";
// Cargar variables de entorno
dotenv.config();
/// Funcionalidad de la app
async function main() {
  try {

  } catch (error) {
    console.error("[ERROR] Problema detectado en el test:", error.message);
    console.error(error.stack);
  } finally {
    console.log("[OK] Realizando limpieza...");
  }
}
main();

// Iniciar el servidor
app.listen(config.port, () => {
  console.log(`Servidor escuchando en http://localhost:${config.port}`);
});
