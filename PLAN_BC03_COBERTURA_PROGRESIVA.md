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
