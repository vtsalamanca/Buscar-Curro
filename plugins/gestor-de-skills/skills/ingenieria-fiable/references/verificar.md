# Evidencia antes de afirmar que algo está resuelto

## Compuerta de verificación
1. Formular la afirmación: «se guardó», «la prueba pasó», «la fuente está completa», «se publicó versión X», «no cuesta nada».
2. Identificar una prueba adecuada por afirmación: código de salida y log, contenido releído, identificador de publicación, matriz de fuentes, o consulta de tarifa/cuota.
3. Ejecutar la verificación permitida cuando exista la herramienta y autorización, leer el resultado completo y fecharlo.
4. Si falta evidencia, usar lenguaje acotado: «preparado», «revisado estáticamente», «pendiente de probar», «fuente parcial».
5. Antes de cambiar un plugin, comprobar identidad y versión/release actual; tras actualizar, releer manifiesto y rutas nuevas; mantener referencia a la versión anterior para recuperar si aparece un defecto.
6. Distinguir validación de una skill (Markdown, estructura, rutas, ausencia de scripts) de funcionamiento end-to-end del sistema objetivo. La segunda requiere ejecución observada, no deducción.
7. No afirmar recepción push, apertura de sesión, acceso privado, cobertura exhaustiva ni operación continua si solo hay estados indirectos.

## Informe corto
- Verificado: actividad, fecha, artefacto y evidencia.
- Parcial/no probado: por qué y qué falta.
- Riesgos residuales y costes adicionales, incluyendo «desconocido».
- Rollback: ID de versión previa o archivo/cambio reversible, sin destruir datos.
