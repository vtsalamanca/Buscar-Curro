# Desarrollo eficiente: selección de entorno y coste total

## Regla de decisión antes de ejecutar
Antes de pedir que el usuario modifique un archivo o ejecutar un diagnóstico, comparar alternativas disponibles según: (1) calidad y seguridad de evidencia, (2) coste marginal real y riesgo de facturación, (3) tiempo humano y número de acciones, (4) consumo de créditos/cuotas, (5) reutilización de resultados. Elegir la alternativa de menor coste total que alcance la evidencia necesaria; no trasladar cargas al usuario solo para ahorrar créditos al asistente.

## Orden orientativo (no rígido)
1. Reutilizar archivos, informes, código y diagnósticos existentes; revisar capacidades del complemento/skills y herramientas ya disponibles.
2. Razonamiento, inspección estática, pruebas con datos sintéticos y análisis local sin red mediante herramientas gratuitas ya accesibles.
3. Si se requiere consultar una fuente pública real, combinar las comprobaciones en una exploración acotada; no invocar el runner remoto para cada regex o búsqueda en un archivo ya descargado.
4. Desarrollar y depurar en un entorno local adecuado y autorizado (propio entorno de análisis o equipo del usuario cuando haya acceso), con tests reproducibles.
5. Usar repositorios y CI/GitHub Actions para versionado, integración y tareas programadas definitivas; diagnósticos remotos solo cuando el entorno remoto sea parte de la hipótesis o resulte realmente más eficiente.
6. Codex/Work exclusivamente si aportan capacidades indispensables o ventaja cuantificable; la selección no autoriza ningún gasto adicional.

## Agrupación y bucle corto
- Establecer preguntas diagnósticas por adelantado; preparar una prueba que responda varias sin repetir descargas, commits y ejecuciones.
- Guardar en memoria temporal reutilizable resultados públicos no sensibles (p. ej. HTML/JS descargados, hash, fecha, URL), con controles de caducidad. No almacenar credenciales, tokens, cookies ni datos personales en repositorios públicos, artefactos ni logs.
- Probar análisis estático, expresiones regulares, sintaxis y casos límite localmente antes de desplegar. Si una ejecución devuelve «success» pero ninguna evidencia relevante, registrar resultado INCONCLUSO y corregir el diseño del diagnóstico; no encadenar confirmaciones vacías.
- Ante dos iteraciones consecutivas sin evidencias útiles, detener el bucle y reconsiderar hipótesis, fuentes y entorno; no volver a pedir al usuario el mismo ritual.
- Agrupar instrucciones para el usuario solamente cuando realmente tiene que intervenir. Preferir una acción única frente a instrucciones fragmentadas y repetitivas; cuando pida guía paso a paso, respetarla.

## GitHub y privacidad
- Un repositorio público con runner Linux estándar puede reducir minutos facturables, pero no convierte la plataforma en almacenamiento privado: separar completamente código de mensajes de menores y datos de acceso.
- Reducir permisos, duración, reintentos y frecuencia; bloquear servicios o runners pagables sin aprobación específica y verificación de tarifa.
- Antes de ejecutar flujos con secretos, revisar qué código y ramas los reciben y evitar exponerlos a contribuciones no confiables. No imprimir encabezados Authorization, cuerpos escolares ni URLs con tokens.
- Medir coste de almacenamiento y límites reales en vez de afirmar coste cero universal por usar repositorio público.

## Aprendizaje y cierre
Documentar hipótesis -> experimento -> evidencia -> corrección, el número de intervenciones humanas y ejecuciones evitables. Tras el cambio, convertir errores metodológicos en reglas transferibles a próximos proyectos. Distinguir claramente «diseñado», «inspeccionado», «probado localmente», «integrado» y «ejecutado en producción».

## Caso Educamos (octubre 2026)
Se ejecutaron múltiples workflows de diagnóstico para inspeccionar un JS público, incluyendo búsquedas de cadenas y una expresión regular mal planteada. Esas operaciones podían agruparse y ensayarse localmente antes de consumir tiempo del usuario en ediciones/commits y runners. Los logs de acciones no acreditan una autenticación HTTP ni un endpoint de mensajería si la prueba no lo comprobó. Regla: analizar archivos públicos una vez, procesarlos localmente, llevar a Actions solo la comprobación específica de conectividad/integración.
