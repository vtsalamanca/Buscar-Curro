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

## ETT-01 — agencias públicas y persistencia (19/10/2026)

Ejecución final: https://github.com/vtsalamanca/Buscar-Curro/actions/runs/39174181284 sobre `215050e`. La suite completa superó 43 pruebas y la ejecución restauró el histórico anterior: **0 nuevos, 0 cambiados, 0 fallos**.

| Fuente | Acceso real desde Actions | Resultado del conector acotado |
|---|---|---|
| Tratem | **HTTP_HTML_verificado**, 125 enlaces | 2 relevantes; el anuncio antiguo sin cierre se marca histórico. |
| Adecco | **HTTP_HTML_verificado**, 9 enlaces de listado | 1 relevante; 1 ficha con `JobPosting`; contradicciones de jornada/contrato se conservan como calidad del dato. |
| Eurofirms | **HTTP_HTML_verificado**, 98 enlaces | 0 relevantes en 4 fichas; no equivale a catálogo vacío. |
| Randstad | **HTTP_HTML_verificado**, 30 enlaces | 1 relevante en 3 fichas. El 403 previo no apareció en el runner; acceso todavía potencialmente variable. |
| Manpower | **HTTP_HTML_verificado**, 3 enlaces | 0 relevantes; las 3 fichas contenían `JobPosting`. |
| Gi Group | **HTTP_HTML_verificado**, 13 enlaces | 0 relevantes; 4 fichas con `JobPosting`; redirecciones a catálogo ajeno se descartan explícitamente. |

La recuperación del estado usa artefactos gratuitos con retención de 30 días, sin escribir en `main`. Valida ZIP, tamaño y esquema, y no reenvía el Bearer token al host firmado de Azure/GitHub. La primera descarga reveló un 401 en https://github.com/vtsalamanca/Buscar-Curro/actions/runs/39169993066; la corrección quedó verificada en los runs posteriores.

La persistencia transversal de BT-01B también quedó demostrada: https://github.com/vtsalamanca/Buscar-Curro/actions/runs/39174196772 creó una línea base de 40 documentos y https://github.com/vtsalamanca/Buscar-Curro/actions/runs/39174265185 restauró el artefacto y devolvió **0 nuevos / 0 cambiados**. Ambos workflows siguen siendo exclusivamente manuales.

## BC-02 — métricas y cobertura progresiva (19/10/2026)

Run final: https://github.com/vtsalamanca/Buscar-Curro/actions/runs/39214493868 sobre `f08fdd8`. Resultado: 50 tests, 6 fuentes accesibles, 19 peticiones, 4.697.241 bytes, 35,802 s HTTP, 13 fichas examinadas en esa pasada, 0 errores y 0 nuevos/0 cambiados. El cálculo legado con las mismas respuestas habría requerido 25 peticiones, 6.686.792 bytes y 48,021 s: reducciones del 24,0 %, 29,8 % y 25,4 % respectivamente.

La cola conservó 36 fichas distintas ya comprobadas, 137 pendientes y 107 descartes preliminares de sectores suspendidos. La semilla educativa Adecco se protege del término genérico «transporte»; el run https://github.com/vtsalamanca/Buscar-Curro/actions/runs/39213963243 verificó su recuperación y el run final confirmó que no reaparece como nueva. El índice geográfico validó 259 municipios; datos ausentes o desconocidos permanecen para revisión.

Peticiones condicionales: hubo ETag en 2/19 respuestas finales y ningún `Last-Modified`, sin prueba de `304`. Se mantienen desactivadas hasta acreditar ahorro real. No se modificó ATE, no se añadieron dependencias, navegador, credenciales, programación recurrente o acciones sobre candidaturas.

## BC-03 — cobertura final por fuente (19/10/2026)

Run final: https://github.com/vtsalamanca/Buscar-Curro/actions/runs/39255609713 sobre `b948d94`. Superó 54 pruebas y restauró el histórico acumulado con 0 nuevos, 0 cambiados y 0 pendientes activos.

| Fuente | Páginas públicas verificadas | Candidatos | Fichas únicas visitadas | Filtrados | Errores / no listado | Pendientes |
|---|---:|---:|---:|---:|---:|---:|
| Tratem | 1 | 126 | 102 | 24 | 0 | 0 |
| Adecco | 1 | 10 | 10 | 0 | 0 | 0 |
| Eurofirms | 2 | 104 | 79 | 6 | 19 errores | 0 |
| Randstad | 2 | 61 | 60 | 0 | 1 no listado | 0 |
| Manpower | 1 | 3 | 3 | 0 | 0 | 0 |
| Gi Group | 1 | 13 | 13 | 0 | 0 | 0 |

Total: 317 candidatos clasificados, 267 fichas visitadas, 30 descartes preliminares, 19 errores explícitos y 1 enlace desaparecido. Eurofirms y Randstad son las únicas fuentes con paginación pública realmente demostrada en esta fase. «Pendientes 0» no significa cobertura completa del portal cuando su paginación no está expuesta o quedan errores.

La última ronda realizó 8 peticiones, descargó 2.876.702 bytes y empleó 17,429 s HTTP sin repetir fichas conocidas. Las siete rondas BC-03 sumaron 307 peticiones, 62.652.365 bytes y 515,756 s HTTP. Se conserva el índice de 259 municipios y las ofertas con localidad desconocida no se descartan silenciosamente.

## BC-06 — BOE por fechas (25/10/2026)
Nueva ruta oficial https://www.boe.es/datosabiertos/api/boe/sumario/{fecha}
(protocolo XML) verificada desde Debian; reemplaza el enfoque dependiente de un
único BOE histórico para descubrimiento. Consultas locales 18–24/10/2026:
6 ediciones disponibles, domingo sin publicación, 1539 títulos examinados,
0 candidatos tras depuración de filtros. Primera versión daba 7 falsos
positivos; se corrigieron antes de incorporar código. Son coincidencias de
títulos, no cobertura exhaustiva de ofertas. Nuevo workflow solo manual,
estado 30 días, sin cron. Informe: IMPLEMENTACION_BC06_BOE_2026-10-25.md.
