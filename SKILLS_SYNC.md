# Sincronización de skills — auditoría 2026-10-19

## Hallazgo verificado
- **GitHub**: `skills/organizaciondeltrabajo/SKILL.md` versión **0.1.6** (historial de cambios de desarrollo local y validación remota).
- **Plugin instalado en ChatGPT**: `gestor-de-skills` versión **0.4.2**, release `pluginrel_6ad5f91ebbcc8191a936456aad661a0a`, incluye una **copia empaquetada** de `skills/organizaciondeltrabajo/SKILL.md` versión **0.2.0**. Se pudo leer la skill desde ChatGPT. **No se actualiza por cambios al repositorio**: la skill forma parte de una release, no un enlace vivo.
- **Codex Windows**: no se pudo inspeccionar la copia local en esta sesión; Remote Desktop Commander indicó **sin dispositivos conectados**. No atribuir a Codex una versión no verificada.
- Los dos documentos son **divergentes**, no asumir que versión semántica mayor incluye todos los cambios de la otra rama.

## Fuente de verdad objetivo y procedimiento
Elegir GitHub `vtsalamanca/Buscar-Curro/skills/organizaciondeltrabajo/SKILL.md` como **fuente editable canónica futura**; conservar historiales y fusionar explícitamente los cambios útiles del plugin 0.2.0 y repositorio 0.1.6 **antes de publicar una nueva versión común**.
1. En cada invocación cuando exista conexión GitHub: leer el archivo desde GitHub y verificar su campo `version`/SHA. Si el entorno no puede acceder, usar la copia empaquetada y etiquetarla como posiblemente desactualizada; no presentar una sincronización falsa.
2. Para el plugin ChatGPT instalado: publicar una **nueva release** tras editar el paquete desde Plugin Creator (requiere reconstruir y subir archive ZIP/tar.gz; la publicación de un commit en GitHub no actualiza automáticamente la release). No afirmar live update si no se ha implementado lectura dinámica verificada.
3. Para Codex local: `git fetch` / avance rápido seguro de la única copia local, comprobar si Codex lee la skill desde ese directorio o desde otra instalación y configurar referencia real al fichero de repositorio si el cliente lo soporta; no sobrescribir ficheros locales ni inventar enlaces. La sincronización del repo y la invocación de skill deben verificarse en el entorno.
4. Mantener una prueba de consistencia: comprobar versiones y hashes GitHub/ChatGPT/Codex y reportar divergencias. Evitar actualizar cada copia a mano si se puede leer GitHub al uso, pero no suponer que plugins empaquetados tienen lectura dinámica.
5. Presupuesto 0 €; no introducir sync automática con runner/servicio de pago y no activar workflows para esta gestión.

## Estado
**Auditoría efectuada; centralización total pendiente.** No se ha modificado ni publicado la release del plugin; Codex local no verificado. Este documento evita atribuir actualización automática a un cambio de GitHub.
