# Diagnóstico de causas y fallos de integración

1. Describir síntoma exacto y evidencia: URL/ruta, operación, hora, respuesta/status, traza y último estado correcto; censurar datos privados.
2. Separar capas: origen o portal; red; autenticación y autorización; navegador o API; extracción; filtrado; deduplicación; almacenamiento; entrega. Un error en una capa no acredita un fallo de otra.
3. Comparar con la última operación comprobada, cambios recientes, documentación y pruebas existentes. Distinguir caída real de fuente, rechazo del cliente, sesión no disponible, dato mal interpretado y problema temporal del entorno.
4. Formular una hipótesis falsable y elegir una comprobación mínima, preferiblemente estática o simulada. Modificar una variable cada vez. No encadenar arreglos especulativos.
5. Reintentar **como máximo una vez** ante fallo transitorio y usar **una alternativa legítima diferenciada** si puede aportar evidencia. Ante autenticación/seguridad, detener la vía afectada, preservar resultados independientes y ofrecer reanudación autorizada.
6. Registrar para cada fuente COMPLETA / PARCIAL / NO CONSULTADA / FALLIDA y para cada incidencia CONFIRMADO / HIPÓTESIS / NO COMPROBADO. «Sin novedades» exige cobertura y comparación suficientes.
7. Si no hay causa identificada, informar «causa pendiente» y evidencia faltante; no declarar reparación. Si varias correcciones consecutivas no funcionan, revisar la arquitectura en vez de repetir.

Ejemplos: un HTTP 403 no demuestra anuncio caducado; un navegador roto no demuestra contraseña incorrecta; una ejecución lanzada no demuestra informe entregado.
