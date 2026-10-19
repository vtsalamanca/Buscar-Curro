# BC-03 — Completar cobertura progresiva sin perder ligereza

Fecha: 2026-10-19. Estado: planificación para ejecución por Codex en el hilo existente. Partir de la rama main posterior a BC-02 (`fb36fe6`) y consultar resultados/artefactos de los runs 39213241555, 39213963243, 39214493868 antes de cambios.

## Objetivo
Agotar de manera progresiva los **137 candidatos pendientes identificados en BC-02** (cifra inicial, puede variar cuando las fuentes cambian), ampliar cobertura mediante paginación pública donde se verifique y registrar si el catálogo está realmente completo o qué parte sigue sin consultar. Preservar selección de empleos de ATE, psicología no sanitaria, educación, menores, intervención social y discapacidad. Almacén/logística sigue suspendido.

## Reglas de ejecución
1. Auditar primero estado, cola y métricas BC-02. Revisar explícitamente el efecto de semillas permanentes y los 107 predescartes por títulos: garantizar que ninguna oferta de interés evidente fue excluida por falsos positivos. No restaurar un estado distinto ni reiniciar la cola sin fundamento.
2. Avanzar cola persistente por rondas con límites seguros configurables, priorizando nuevos enlaces relevantes, luego pendientes antiguos, y refrescando conocidos solo cuando exista señal de cambio/caducidad o intervalo justificable. No repetir siempre primeras fichas. La cifra 137 es pendiente inicial, no garantía de que todos los enlaces son ofertas.
3. Comprobar paginación por fuente (Tratem, Adecco, Eurofirms, Randstad, Manpower, Gi Group) en HTTP público sin autenticación, evitando suposiciones sobre URLs o parámetros. Usar paginación real solo cuando exista evidencia; paginación JS sin endpoint público viable permanece parcial, sin montar browser automáticamente.
4. Separar métricas `listings_pages`, `listing_links`, `candidate_urls`, `detail_fetches`, `unique_candidates_visited`, `pending_candidates`, `preliminarily_filtered`, `errors`, `requests`, `bytes`, `http_seconds` por fuente; registrar cobertura por páginas y candidatos con denominador verificado. No afirmar exhaustividad si paginación no verificada o existen pendientes.
5. Incrementar tamaño de lote solo si métricas muestran beneficio y fuentes toleran peticiones. Límite configurable de peticiones/páginas/bytes/tiempo por ejecución; reintentos controlados con esperas y no ante fallos permanentes; no perder estado si una fuente falla. Respetar las condiciones y límites del sitio.
6. Filtro de 259 municipios por CSV precargado; desconocidas/ambiguas quedan en revisión. No geocodificación de pago ni mapas en cada oferta. Distinguir distrito/barrio de municipio y no declarar distancia de carretera.
7. Idempotencia entre varias ejecuciones independientes (>=2), restauración de estado válida, sin falsos nuevos/cambiados; conservación de corrección Adecco; pruebas de paginación repetida, desplazamientos y errores parciales, sin romper ATE y BT-01B.
8. Pruebas locales completas + workflow manual acotado, documentar resultados por fuente, URLs de Actions y commits. Si no se puede demostrar avance debido a cambios del portal, explicar bloqueo específico en vez de fabricar cobertura.

## Restricciones
Coste adicional 0 €, priorizar biblioteca estándar y HTTP ligero, sin dependencias innecesarias, sin acciones sobre candidaturas, autenticación privada, bypass ni nuevos repositorios. Workflow manual, sin cron, avisos o informes personalizados. No alterar historial ni el CSV geográfico salvo corrección demostrada. Usar proyecto local ya existente.

## Salida
Evidencia comparativa antes/después de fichas únicas examinadas, cola pendiente, páginas verificadas, errores, peticiones, bytes y tiempo. Diferenciar 'todos los candidatos detectados procesados' de 'todas las ofertas del portal', que requiere verificar paginación.

## Política general aplicable — 19/10/2026
Leer también `POLITICA_EFICIENCIA_PRESUPUESTO_CERO.md` antes de programar o ejecutar BC-03. Este documento establece como futuros límites operativos un cron al día, 15 minutos máximo, 10 MB totales de artefactos por ejecución, 7 días de diagnósticos y un solo runner operativo simultáneo. **No activar ahora** estos mecanismos ni recortar el histórico de 30 días sin una sustitución segura; validar cada límite y la facturación primero. Las ejecuciones manuales de prueba requieren autorización y esta actualización documental no la concede.

## Resultado técnico — 19/10/2026

**BC-03 ejecutado y verificado.** Se restauró el artefacto de BC-02 sin reiniciar el histórico y se clasificó un universo final de 317 candidatos detectados: 267 fichas únicas descargadas, 30 descartes preliminares seguros, 19 errores conservados para reintento y 1 enlace de Randstad ya ausente del listado. La cola activa quedó en **0 pendientes**; esto significa que no quedan candidatos detectados sin clasificar, no que se haya demostrado la exhaustividad completa de cada portal.

- Paginación pública comprobada: Eurofirms, 2 páginas (101 enlaces y 104 candidatos); Randstad, 2 páginas (60 enlaces y 61 candidatos). Tratem, Adecco, Manpower y Gi Group solo expusieron una página verificable; no se inventaron parámetros.
- Cobertura final: Tratem 102 visitados y 24 filtrados; Adecco 10 visitados; Eurofirms 79 visitados, 6 filtrados y 19 errores; Randstad 60 visitados y 1 no listado; Manpower 3 visitados; Gi Group 13 visitados.
- La última ronda idempotente realizó 8 peticiones de listado, 2.876.702 bytes y 17,429 s HTTP, sin descargar fichas conocidas, sin pendientes y con 0 nuevos/0 cambiados. Los 19 errores persistentes se muestran como errores, nunca como ausencia de ofertas.
- Las siete rondas de diagnóstico y avance consumieron en conjunto 307 peticiones, 62.652.365 bytes y 515,756 s HTTP. La cobertura única pasó de 36 fichas examinadas en BC-02 a 267 en BC-03.
- Correcciones aplicadas durante las rondas: clasificación HTML basada en título para evitar contaminación de menús; identificador real de Gi Group; refresco de conocidos no antes de siete días; clasificación `not_listed` de enlaces desaparecidos; conservación de errores; y migración automática desde el artefacto BC-02.
- Commits funcionales: `24998e7`, `45d48c9`, `297c8d8`, `7ff7e69` y `b948d94`.
- Evidencias Actions: [ronda inicial](https://github.com/vtsalamanca/Buscar-Curro/actions/runs/39245609244), [paginación y filtros](https://github.com/vtsalamanca/Buscar-Curro/actions/runs/39251098099), [avance amplio](https://github.com/vtsalamanca/Buscar-Curro/actions/runs/39253200014), [segunda ronda amplia](https://github.com/vtsalamanca/Buscar-Curro/actions/runs/39253677115), [casi agotada](https://github.com/vtsalamanca/Buscar-Curro/actions/runs/39254699940), [cola agotada](https://github.com/vtsalamanca/Buscar-Curro/actions/runs/39255134235) y [verificación final](https://github.com/vtsalamanca/Buscar-Curro/actions/runs/39255609713).

La suite final superó 54 pruebas, incluidas las regresiones ATE, BT-01B y ETT-01. El workflow sigue siendo exclusivamente manual, sin cron, credenciales privadas, navegador, notificaciones, candidaturas ni servicios de pago.
