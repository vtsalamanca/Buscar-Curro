# Fuentes automáticas

## ATE público Toledo — 18/10/2026

Acceso automático verificado desde GitHub Actions: https://github.com/vtsalamanca/Buscar-Curro/actions/runs/39152509426 . Tres pruebas superadas y descarga pública del PDF de Toledo validada por firma PDF; 865225 bytes, SHA256 e016ae338b95cd8f81179918a2ab12785a89f3c584aa593aab7d3555dfd5f68d. La misma huella se obtuvo en la prueba local independiente.

ate_public.py descubre el enlace actual desde la página de categoría; limita host y HTTPS incluso en redirecciones, tamaño y espera. No guarda ni publica datos de aspirantes. Ausencia del documento es fallo, nunca «sin novedades».

Alcance: acceso a página y documento público. No interpreta fechas, vigencia, posiciones personales o ampliaciones; tampoco prueba cobertura de todas las publicaciones ATE. Pendientes: comparación persistente de huellas, extracción de anuncios/fechas y entrega del resumen. Workflow manual o al cambiar sus archivos; sin programación recurrente.

## Decisión de alcance

Seguimiento privado de InfoJobs aparcado por petición del usuario; usar avisos de vtsalamanca@gmail.com. Conector de Gmail accesible en ChatGPT, sin conexión de Gmail a GitHub verificada. Otros colectores públicos pendientes de implementación y prueba individual. No usar servicios tarificados sin autorización específica.

## BT-01A — viabilidad pública desde GitHub Actions (18/10/2026)

Ejecución válida: https://github.com/vtsalamanca/Buscar-Curro/actions/runs/39163691686 sobre commit `67cbea0`. Runner estándar `ubuntu-24.04`, permisos `contents: read`, sin secretos, login, cookies, JavaScript, reintentos ni programación recurrente. Nueve pruebas unitarias superadas y diagnóstico completo; artefacto `bt01a-public-source-viability` (ID `12149183682`, SHA-256 ZIP `86795d842a8c188039de4b5e1d064cab0be518eec9b66e4ccfc7f704c73e36c5`, retención 7 días).

| Fuente | Resultado runner | Evidencia y límite |
|---|---|---|
| DOCM | **verificada_desde_runner** | HTTP 200 y enlaces relevantes. Prueba acceso a búsqueda pública, no parámetros de consulta ni extracción completa. |
| BOE | **verificada_desde_runner** | HTTP 200 sobre caso oficial `BOE-A-2026-7237` y enlaces relevantes. Prueba lectura documental, no descubrimiento exhaustivo. |
| BOP Toledo | **verificada_desde_runner** | HTTP 200 y enlaces relevantes en buscador público. Paginación y descarga sistemática pendientes. |
| JCCM últimas modificaciones | **verificada_desde_runner** | HTTP 200 y enlaces relevantes. Falta implementar filtrado y recorrido. |
| Empleo CLM | **parcial** | HTTP 200 y página relevante, sin enlaces de resultados confirmados por el diagnóstico estático. |
| Empléate | **bloqueada** | `network_error` desde el runner en el único intento acotado. Puede ser transitorio; no se repitió sin diagnóstico nuevo. |
| Ayuntamiento de Toledo | **parcial** | HTTP 200; carga pública con señal de login. No se confirmó acceso autónomo a todas las fichas. |
| Sede de Nambroca | **bloqueada** | Respuesta `HTTPError:302`; el flujo de redirección no produjo página pública analizable. |
| Ayuntamiento de Aranjuez | **verificada_desde_runner** | HTTP 200 y enlaces relevantes en documentación de empleo público. |
| Centro Trama | **parcial** | HTTP 200; carga pública con señal de login. Catálogo/fichas requieren prueba específica antes de implementar. |
| ILUNION VidaSénior | **verificada_desde_runner** | HTTP 200 y enlaces relevantes en el catálogo. |
| Cruz Roja | **parcial** | HTTP 200; carga pública con señal de login. No se confirmó recorrido de resultados/fichas sin sesión. |
| ACCEM | **no_probada** | No existe en el inventario una URL oficial directa de vacantes validada; la página de programas no se usó como falso catálogo. |

El run https://github.com/vtsalamanca/Buscar-Curro/actions/runs/39163408797 queda **descartado para clasificar fuentes**: una regla inicial confundía la etiqueta HTML normal `meta robots` con una verificación humana. El defecto se corrigió y quedó cubierto por regresión antes del run válido.

Advertencias no bloqueantes del runner: GitHub forzó a Node.js 24 dos actions que aún declaran Node.js 20, y anunció migración futura de la etiqueta `ubuntu-latest`. Deben revisarse al mantener el workflow, pero no invalidaron sus pasos ni resultados. `verificada_desde_runner` significa página pública y enlaces relevantes accesibles; no equivale a conector terminado, cobertura completa ni oferta vigente.

## BT-01B — conectores públicos (18/10/2026)

Ejecución de cierre: https://github.com/vtsalamanca/Buscar-Curro/actions/runs/39165959658 sobre commit `b45f02e`. Los 20 tests seleccionados por el workflow terminaron correctamente; el artefacto `bt01b-public-source-results` (ID `12150139921`, 13386 bytes, SHA-256 ZIP `45909783b7b9d0bb5cff28c6422569263e67c80c1b4465a8fe0ab2db3955c68e`) conserva durante 7 días ejecuciones por fuente, estado, delta y reporte detallado. La suite local completa superó 31 pruebas, incluidas las de autenticación y fuente pública ATE existentes.

| Fuente | Estado BT-01B en runner | Resultado y límite comprobado |
|---|---|---|
| DOCM | **operativa_acotada** | 3 casos históricos recuperados por URL oficial; no existe aún descubrimiento exhaustivo por fecha/sumario. |
| BOE | **operativa_documental** | 1 caso oficial relevante; lectura y clasificación funcionan, pero el catálogo no se recorre de forma exhaustiva. |
| BOP Toledo | **acceso_sin_resultados_extraibles** | 8 enlaces candidatos en el buscador, 0 documentos relevantes. El formulario/paginación requiere un método específico; no equivale a ausencia de publicaciones. |
| JCCM | **operativa_incremental** | 3 enlaces candidatos y 2 documentos relevantes tras excluir navegación genérica y falsos positivos. Cobertura limitada a últimas modificaciones. |
| Empleo CLM | **parcial_sin_catalogo_estatico** | Página consultada, 0 enlaces de resultado extraíbles sin JavaScript/parámetros adicionales. |
| Ayuntamiento de Toledo | **operativa_listado** | 36 enlaces candidatos y 2 bolsas relevantes de Educación/Trabajo Social. No se afirma vigencia cuando falta cierre explícito. |
| Ayuntamiento de Aranjuez | **operativa_semilla** | Caso histórico de Trabajador Social recuperado; un recurso enlazado devolvió tipo de contenido no HTML. No hay recorrido completo del catálogo. |
| Centro Trama | **operativa_catalogo** | 18 enlaces candidatos y 10 documentos relevantes; hay anuncios históricos y no todas las fichas se descargan en una ejecución acotada. |
| ILUNION VidaSénior | **operativa_catalogo** | 10/10 enlaces clasificados por discapacidad. Son candidatos, no recomendaciones: titulaciones y distancia deben comprobarse antes de actuar. |
| Cruz Roja | **parcial** | 3 enlaces candidatos, 0 documentos relevantes; una ficha respondió `HTTPError:302` con redirección bloqueada por la lista segura. |

Las ejecuciones `39165252983`, `39165510317` y `39165713985` se conservan como iteraciones diagnósticas. Permitieron corregir el término ATE para que solo coincida como acrónimo, reconocer `trabajador/a social`, extraer enlaces fuera de bloques semánticos y eliminar menús genéricos de JCCM/Toledo. La ejecución de cierre anterior es la referencia válida.

El workflow `.github/workflows/bt01b-public-sources.yml` solo admite `workflow_dispatch`, usa runner estándar y permisos `contents: read`; no contiene `schedule`, secretos, login ni servicios de pago. Los resultados no activan avisos ni candidaturas. “Sin resultados relevantes” significa que la consulta respondió pero el extractor no obtuvo documentos que pasaran sus reglas; `consulta_fallida` se registra por separado.
