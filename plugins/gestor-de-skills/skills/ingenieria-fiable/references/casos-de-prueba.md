# Casos de aceptación de la adaptación (validación sin red)

| Caso | Entrada simulada | Resultado esperado |
| --- | --- | --- |
| Habitual | Mejora de filtro con historial verificable | Plan breve, prueba de regresión, cambio mínimo y verificación |
| Resultado vacío | Fuente responde con 0 ofertas válidas | 0 ofertas, sin confundirlo con error |
| Error de acceso | Fuente privada muestra login/CAPTCHA | Detener acceso privado, continuar fuentes públicas, incidencia pendiente |
| Fuente inaccesible | Timeout o 403 real | Una comprobación de contexto y una alternativa autorizada, matriz parcial |
| Dependencia ausente | Test no encuentra herramienta local | No declarar prueba pasada ni instalar automáticamente |
| Coste desconocido | Job con proveedor/runner de precio incierto | Bloquear ejecución, indicar tarifa/saldo/coste por verificar |
| Duplicados | Dos enlaces de una misma vacante | Un registro único, historial preservado |
| Oferta caducada | Buscador reciente, página original cerrada | No clasificar como vacante nueva vigente |
| Guardado fallido | Actualización devuelve error | No afirmar historial actualizado, conservar datos para recuperación |
| Rollback | Actualización de plugin no supera relectura | Mostrar fallo y referencia a release anterior para restauración autorizada |

Esta tabla define expectativas para probar el contenido y futuras implementaciones; no equivale a haber ejecutado búsquedas reales ni tests de un programa concreto.
