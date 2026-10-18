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

## Nuevas evidencias web — descubrimiento y alcance, 18/10/2026
- **Adecco, resuelta la duda del enlace de ficha.** Página real accesible: https://www.adecco.com/es-es/ofertas-trabajo/coordinador-a-de-transporte-escolar-y-acompanantes-20h-toledo-toledo/feff860faf43f8aa1b13e4812d309296 . Tiene ID `FEFF860FAF43F8AA1B13E4812D309296`, ubicación Toledo, sector Educación/Formación, salario 712,25 € brutos/mes por 20 h/semana, horario partido de lunes a viernes, fijo discontinuo en descripción aunque etiqueta resumen dice temporal/tiempo completo (**contradicción interna del portal; prevalece detalle sujeto a confirmación de empresa**), bachillerato, experiencia con niños valorada, certificado negativo de delitos sexuales y vehículo propio en algunas rutas. Parece afín al perfil, **pero fecha de publicación/cierre y vigencia no verificadas; NO enviar candidatura ni anunciarla como vigente**. Método inicial HTTP GET ficha y enlazado desde listado; necesidad de navegador no demostrada.
- **Randstad, ruta real de paginación:** https://www.randstad.es/candidatos/ofertas-empleo/p-toledo/c-toledo/pg-2/ muestra segunda página real con 6 entradas adicionales al bloque de 30. Catálogo provincia https://www.randstad.es/candidatos/ofertas-empleo/p-toledo/ incluye filtros por localidad y puesto, y las cifras cambian. Comprobar paginación y deduplicación por ficha.
- **Gi Group:** https://es.gigroup.com/ofertas-de-trabajo/castilla-la-mancha-re/toledo-pr/toledo-ci/ (ruta distinta de Illescas) muestra 11 últimos puestos; filtro por «ciudad» puede listar **puestos situados fuera del municipio nombrado**, por lo que ubicación debe tomarse de cada ficha, nunca inferirse de la URL de búsqueda. Los listados muestran 14 puestos en Illescas, 15 en Valmojado, etc., con coincidencias: evitar sumarlos como ofertas distintas. No afirmar cobertura provincial exhaustiva a partir de estos catálogos por ciudad.
- **Eurofirms:** https://jobs.eurofirms.com/es/es/trabajo/toledo muestra 36 resultados en última lectura y filtros por población, jornada, modalidad, fecha, discapacidad y «tipo de oferta» (selección/fundación/equipo). Cifras no estables; fichas/IDs y criterios de aceptación pendientes de runner.
- Regla práctica: ficha pública leíble vía navegador textual/Web **no es prueba** de `urllib` runner. Ejecutar primero `HTTP GET` de URL exacta y contar enlaces/atributos estructurados; datos contradictorios se marcan `requiere_verificacion`; no activar navegador ni acciones de candidatura.

## Riesgos nuevos comprobados en navegación pública (18/10/2026)
- **Randstad:** URL de listado provincial devuelve resultados indexables y ruta de paginación `/p-toledo/c-toledo/pg-2/`, pero apertura directa del listado `/p-toledo/` desde el lector web devolvió **HTTP 403** en un intento. Estado: **acceso variable/parcial según cliente**, no afirmar `urllib` viable. Codex debe registrar respuesta sin forzar protección, buscar vías públicas menos costosas y, si se bloquea, dejar aparcada.
- **Gi Group:** enlace de ficha mostrado en https://es.gigroup.com/ofertas-de-trabajo/castilla-la-mancha-re/toledo-pr/toledo-ci/ para La Puebla de Montalbán (URL destino `/ofertas-de-trabajo-detalle/la-puebla-de-montalban-toledo-dependiente-a-pescaderia-la-puebla-de-montalban/101001/`) **redirigió a un catálogo de La Puebla de Alfindén, Zaragoza** en el lector web. Importante: enlaces de ofertas vencidas pueden redirigir a otra localidad; validar destino final, provincia y coincidencia real de título, no suponer que un HTTP 200 tras redirección sea una ficha válida. Detectar `redirected_to_unrelated_catalog` y no producir candidato; sin evasión de controles.
- **Adecco:** ficha completa de coordinación escolar (ref `FEFF860FAF43F8AA1B13E4812D309296`) abre en HTML, pero campos de jornada/contrato del resumen contradicen el detalle. Señalar `datos_contradictorios` en vez de elegir silenciosamente uno.
**Nuevos tests recomendados:** 403 por cliente en listado Randstad, redirección de ficha a municipio/provincia sin relación en Gi Group y contrato/jornada inconsistentes en Adecco.

## Reutilización de estándares y bibliotecas — evaluación previa (18/10/2026)
**Hallazgo prioritario: schema.org/JobPosting** (https://schema.org/JobPosting) y guía oficial Google https://developers.google.com/search/docs/appearance/structured-data/job-posting . Las fichas de empleo PUEDEN publicar un bloque HTML `<script type="application/ld+json">` con `@type: JobPosting`, `title`, `datePosted`, `validThrough`, `hiringOrganization`, `jobLocation`, `employmentType`, `baseSalary`, `qualifications`. **Es un estándar, no una API que garantice que las seis ETT lo utilicen.** Instruir a Codex a detectarlo primero en HTML real de cada ficha y validar contenido/localidad; en ausencia usar parser HTML normal, sin navegador. Mejor esfuerzo muy barato con Python `html.parser` + `json` de biblioteca estándar.
**Candidato de código abierto:** https://github.com/speedyapply/JobSpy , paquete https://pypi.org/project/python-jobspy/ , licencia MIT y PyPI 1.3.0 (08/10/2026). Soporta principalmente LinkedIn/Indeed/Glassdoor y otros tableros, **no declara soporte para Tratem, Adecco, Eurofirms, Randstad, Manpower o Gi Group**. Ofrece agregación de resultados con dependencias adicionales; **no instalarlo ahora** ni emplearlo para superar restricciones/rate limits. Considerarlo únicamente para fase posterior de portales generales tras auditoría de mantenimiento, licencia, límites, fiabilidad y coste de dependencias. Para ETT-01 preferir los extractores HTML actuales y parser compartido de JobPosting.
**Orden práctico Codex ETT-01A:** (1) petición HTTP a ficha pública real, (2) detectar `application/ld+json` y `@type=JobPosting`, incluyendo `@graph` y arrays, (3) validar campos y vigencia, (4) si faltan, HTML semántico con enlaces y etiquetas, (5) explorar feeds/APIs públicas documentadas sólo si aportan ventaja, (6) JS/browser como excepción justificada. No asumir por la guía Google que la web devuelve JSON-LD.
**Pruebas:** fixture con JSON-LD JobPosting, JSON-LD no relacionado (BreadcrumbList/Organization), múltiples bloques `@graph`, HTML sin datos estructurados y una ficha caducada. Clasificar correctamente `validThrough`, localidad, agencia intermediaria frente a `hiringOrganization`, y no convertir `datePosted` en plazo de cierre.
**Conclusión:** NO se ha encontrado un conector de código abierto específico verificado para las seis ETT que supere al enfoque HTTP ligero. Sí hay un estándar común reutilizable a comprobar, y JobSpy queda como opción de investigación separada, no dependencia aprobada.

## Auditoría Chat — pruebas concretas de extracción ligera (18/10/2026, 23 h)
Lectura actual de páginas oficiales mediante cliente web, **no captura de HTML bruto ni prueba `urllib` desde GitHub Actions**:
- Tratem https://agenciaempleo.tratem.com/ofertas/ : cada tarjeta del listado contiene título, municipio, vacantes, estado y enlace `/oferta/...`; se pudo seguir a la ficha «Docente Certificado de Habilitación…». Confirmado que en lector web hay estructura documental suficiente para una primera prueba HTTP + HTML.
- Eurofirms https://jobs.eurofirms.com/es/es/trabajo/toledo : 36 resultados indicados, enlaces de puestos numerados en el HTML procesado, fechas y salarios de algunos puestos; filtros provincia/localidad y tipo. **La sección de alertas requiere login**, pero **las fichas del listado público no necesitan login para ser enlazadas**. Asegurar que el parser elige enlaces de oferta, no login/filtros/promoción.
- Adecco ficha https://www.adecco.com/es-es/ofertas-trabajo/coordinador-a-de-transporte-escolar-y-acompanantes-20h-toledo-toledo/feff860faf43f8aa1b13e4812d309296 : lectura pública de puesto, referencia, requisitos y condiciones; discrepancia «tiempo completo / temporal» (encabezado) frente a «20h, fijo discontinuo» (cuerpo). Registrar contradicción, no publicar inferencia de contrato.
- Manpower https://www.manpower.es/es/buscar-trabajo/ciudad/toledo/ : lista pública con enlaces de puesto, localidad y sector, aunque anuncia mantenimiento temporal del login/candidaturas; este aviso **no demuestra que la lectura pública esté bloqueada**.
- **No se puede confirmar la presencia/ausencia de `JobPosting` JSON-LD a partir de la representación de texto de este lector:** el diagnóstico runner deberá inspeccionar el HTML bruto y analizar scripts. No afirmar APIs/feed encontrados.
- Para ETT-01A, en lugar de un navegador por portal, ensayar primero `urllib.request` y parser `html.parser`; evaluar en cada URL si devuelve títulos/IDs/fechas de candidatos reales y un JSON-LD JobPosting, respetar redirects y fallos.
- Añadir pruebas unitarias de exclusión de enlaces de alta/login, de lectura parcial que devuelve HTTP 200 con solo navegación, y de datos contradictorios de Adecco. No activar suscripciones ni enviar candidaturas.
