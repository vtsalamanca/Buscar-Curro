# Buscar-Curro — Ampliación de fuentes ETT (ETT-01)

Fecha: 2026-10-18. Estado: inventario contrastado, **prueba runner y desarrollo pendientes**.

## Alcance autorizado
El usuario quiere ampliar fuentes de empleo con ETT de Toledo, especialmente Tratem y Adecco. No hay autorización para contratar servicios, iniciar sesión con datos privados, enviar candidaturas, activar programación periódica ni notificaciones.

## Fuentes
1. Tratem — https://agenciaempleo.tratem.com/ofertas/ — catálogo público con fecha, vacantes, localidad, estado y fichas.
2. Adecco — https://www.adecco.com/es-es/ofertas-trabajo/localizacion/trabajos-en-toledo — listado público; ejemplo «Coordinador/a de Transporte Escolar y Acompañantes (20h)», sin vigencia/requisitos todavía verificados.
3. Eurofirms — https://jobs.eurofirms.com/es/es/trabajo/toledo — listado provincial y filtros.
4. Randstad — https://www.randstad.es/candidatos/ofertas-empleo/p-toledo/ — localidad, fecha, sector.
5. Manpower — https://www.manpower.es/es/buscar-trabajo/ciudad/toledo/ — catálogo por localidad y fechas.
6. Gi Group — https://es.gigroup.com/ofertas-de-trabajo/castilla-la-mancha-re/toledo-pr/illescas-ci/ — ofertas por localidad.

Todas tienen **acceso a listados comprobado mediante lectura web**, no desde GitHub Actions. No declarar operativas aún.

## ETT-01A — Viabilidad técnica (Codex)
- Recuperar BT-01A/BT-01B y sus tests; conservar íntegro ATE y conectores anteriores.
- Añadir diagnóstico manual, público y acotado sobre seis fuentes con runner estándar público: respuesta real, enlazado de fichas, IDs, fechas, ubicaciones, requisitos, paginación y limitaciones JS.
- Diferenciar listado accesible de fichas realmente extraíbles; registrar 302/bloqueos de forma limpia y continuar.
- No autenticaciones, evasión de retos humanos, bucles intensivos, servicios externos tarificados ni cron.
- Pruebas/regresiones y evidencia reproducible en GitHub Actions.

## ETT-01B — Conectores viables
- Solo implementar las agencias probadas en ETT-01A, con límites de tiempo y tamaño.
- Añadir fuente/ETT/empresa contratante si identificada, ID/URL original, título, municipio, fecha, vigencia, requisitos, jornada, salario si explícito.
- Filtrar sectores activos: ATE, psicología no sanitaria, menores, discapacidad, educación e intervención social. Almacén/logística sigue suspendido; no ocultar un empleo social por palabras genéricas de menús de navegación.
- Distinguir ofertas de anuncios formativos y publicidad; respetar requisitos/habilitaciones y radio máximo 70 km desde Nambroca (no inventar distancias).
- Deduplicar entre agencias y otros portales conservando los enlaces de origen; no fusionar ofertas parecidas sin evidencia.
- Resolver previamente o en paralelo **persistencia entre ejecuciones de GitHub Actions**: BT-01B genera state.json pero su workflow manual no recupera estado anterior. Hacer pruebas de dos ejecuciones y verificar que la segunda no recuenta documentos como nuevos.
- No activar cron, notificaciones ni candidaturas; documentar rutas no viables y pendientes.

## Criterios de aceptación
- Pruebas unitarias y regresión anteriores correctas; ejecución runner válida con resultados por fuente.
- Estado anterior reproduciblemente cargado en segunda ejecución; delta real y errores diferenciados.
- Cero coste adicional, cero credenciales privadas, cero aplicaciones nuevas y ninguna candidatura.
- Actualizar ESTADO_PROYECTO.md, SOURCES_STATUS.md y PLAN_ETT_01.md; devolver commits y enlace de run.

## Investigación previa a Codex — método menos costoso (18/10/2026)
**Métodos propuestos, no validados por runner:** la lectura textual de páginas públicas a través de Web demuestra que se puede recuperar información estructurada o semiestructurada sin ejecutar aquí un navegador interactivo. **No demuestra API oficial, HTML suficiente para cada ficha, ni acceso estable por `urllib` en GitHub Actions.**

| ETT | Evidencia pública en lectura web | Primer protocolo para Codex | Fallback si falla |
|---|---|---|---|
| Tratem | Listado https://agenciaempleo.tratem.com/ofertas/ : enlaces individuales «Ver oferta», localidad, vacantes, fecha y estado «Activa»; anuncios de otros años aparecen como activos | **HTTP GET + parser HTML**, seguir enlaces de ficha, normalizar fechas/año y comprobar fecha real | Navegador solo si fichas no salen por HTTP |
| Adecco | Página Toledo devuelve títulos («Coordinador/a de Transporte Escolar y Acompañantes (20h)») y controles, pero no quedaron demostradas las URLs de ficha en esta inspección | **HTTP GET + parser** para ver si hay `href` o JSON público embebido | Inspección de llamadas JSON públicas; navegador solo si necesario |
| Eurofirms | Página provincial devuelve HTML y contenido; estructura de fichas/enlaces no confirmada | **HTTP GET + inspección HTML**, enlaces, JSON-LD si hubiera | Si resultados solo JS, revisar JSON público legítimo y luego navegador |
| Randstad | https://www.randstad.es/candidatos/ofertas-empleo/p-toledo/ muestra listado con fecha, municipio, salarios, filtros y paginación («ver más», rutas `/pg-2/` observadas en otro segmento) | **HTTP GET + parser HTML**, probar paginación y ficha por URL | Comprobar si listado cargado por endpoint público, sin asumir API |
| Manpower | https://www.manpower.es/es/buscar-trabajo/ciudad/toledo/ muestra ofertas con fechas/localidad y sector | **HTTP GET + parser HTML**, validar enlaces y fichas | JS/JSON público si se precisa; navegador última opción |
| Gi Group | https://es.gigroup.com/ofertas-de-trabajo/castilla-la-mancha-re/toledo-pr/illescas-ci/ devuelve puesto, fecha, contrato, localidad y enlace «Más info»; existen rutas por Toledo ciudad | **HTTP GET + parser HTML**, verificar filtros/rutas y paginación | Navegador solo si ficha o filtros exigen interacción |

**Importante para relevancia:** en Tratem, varias entradas antiguas marcadas «Activa» carecen de evidencia de vigencia actual; no confiar solo en el campo de estado del portal. Randstad y Gi Group muestran muchos puestos de sectores suspendidos: filtrar el texto de la ficha, no descartar toda la fuente.

**Pruebas ETT-01A adicionales para ahorrar cuota:**
- Primer intento HTTP directo con `urllib`, User-Agent identificable, timeout y tamaño; registrar `Content-Type`, estado, cantidad de fichas y campos validados. Descartar HTML con solo menús.
- Comprobar JSON-LD y feeds/APIs oficiales documentadas solo si existen, sin prometerlos ni inventar endpoints.
- Solo ante fallo reproducible justificar navegador completo y estimar coste/tiempo. No montar Playwright por defecto.
- Registrar resultado por fuente: `API_oficial_verificada`, `HTTP_HTML_verificado`, `HTTP_parcial`, `JS_necesario`, `bloqueado`, `no_probado`. Mantener capturas/fixtures pequeñas sanitizadas.
- No basar decisión en páginas indexadas antiguas: las fechas de anuncios pueden ser anteriores, incluso con estado «Activa».

## Verificación adicional de enlaces ficha por HTTP/web pública (18/10/2026)
Investigación desde Chat para reducir consumo de Codex: **NO equivale a prueba urllib en runner ni confirma API oficial**.
- Tratem: https://agenciaempleo.tratem.com/ofertas/ tiene enlaces HTML a fichas. Ejemplo https://agenciaempleo.tratem.com/oferta/docente-certificado-habilitacion-docencia-ab-y-c ; ficha HTML indica publicada **29/10/2025** y que inscripción requiere login; lectura pública libre. Imprescindible comprobar año en ficha: catálogo muestra «29 oct.» sin año y estado «Activa». Categoría docente no implica vigencia ni requisitos cumplidos.
- Eurofirms: https://jobs.eurofirms.com/es/es/trabajo/toledo indexa **36 resultados** en comprobación; ofrece enlaces HTML de fichas y filtros. Ejemplo https://jobs.eurofirms.com/es/es/santa-cruz-de-la-zarza/mozo-a-almacen-063-005159 ficha accesible con fecha 16/10/2026, municipio, jornada, vacantes, salario, requisitos, formación. Ejemplo usado únicamente para **prueba estructural**, sector almacén excluido. Login necesario para inscribirse, **NO para leer ficha**.
- Randstad: https://www.randstad.es/candidatos/ofertas-empleo/p-toledo/ publica lista con fecha, localidad, salario y control «ver más»; ruta de paginación real a comprobar desde runner, no inferir parámetros por otros segmentos.
- Manpower: https://www.manpower.es/es/buscar-trabajo/ciudad/toledo/ incluye enlaces a ficha como https://www.manpower.es/es/empleos/transporte-y-logistica/carretillero-a-sector-alimentacion-h-m-x-/756921 ; sector de ejemplo excluido. En el listado aparece aviso de **mantenimiento de inicio de sesión y solicitudes**: afecta candidaturas, no demuestra cierre de lectura pública.
- Gi Group: https://es.gigroup.com/ofertas-de-trabajo/castilla-la-mancha-re/toledo-pr/illescas-ci/ muestra fecha, sector y enlaces «Más info» en HTML.
- Adecco: https://www.adecco.com/es-es/ofertas-trabajo/localizacion/trabajos-en-toledo muestra títulos y botón aplicar, pero la extracción de enlace de detalle **todavía no se ha confirmado**; mantener hipótesis de JSON embebido/JS y estudiar sin navegador primero.

**Priorización revisada:** en ETT-01A intentar primero HTTP fichas Tratem, Eurofirms y Manpower (URLs de detalles reales verificadas por navegación web), luego Randstad/Gi Group, por último Adecco (incertidumbre de fichas). No usar agentes visuales ni Chromium salvo fallo reproducible del protocolo ligero. Los catálogos actuales están dominados por otros sectores: **no cambiar filtros activos para inflar los hallazgos**.
