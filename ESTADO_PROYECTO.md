# Buscar-Curro — Estado maestro y hoja de ruta

Actualizado: 2026-10-18. Responsable de decisiones: usuario. Presupuesto adicional autorizado: **0 €**.

## Reglas de continuidad
1. Antes de iniciar trabajo consultar este documento, README y evidencias recientes del repositorio.
2. Distinguir siempre **comprobado en GitHub**, **comunicado en conversaciones**, **pendiente de verificar**, **bloqueado** y **descartado**.
3. No repetir tareas resueltas sin documentar por qué; registrar pruebas, URLs oficiales, errores y decisiones.
4. No ejecutar código, activar workflows, solicitar servicios de pago por uso, instalar nada, enviar candidaturas ni modificar accesos sin la autorización correspondiente.
5. Reutilizar GitHub y herramientas ya conectadas. Guardar el estado en Markdown del repositorio, no en sesiones de Chat, Work o un PC concreto.
6. No guardar nunca contraseñas, tokens, cookies, certificados o secretos en el repositorio.
7. Agrupar las intervenciones técnicas para minimizar consumo de tiempo, cuotas y créditos.

## Objetivos
- O1. Consulta fiable de empleo público (ATE/JCCM, DOCM) para Toledo y alrededores.
- O2. Incorporar fuentes adicionales gratuitas de ofertas relacionadas con educación, psicología, menores, intervención social y logística.
- O3. Normalizar ofertas con fuente, fecha, lugar, requisitos, plazo, enlace y cambios detectados.
- O4. Deduplicar, conservar histórico y detectar incidencias sin repetir avisos.
- O5. Emitir un informe resumido y priorizado. El seguimiento privado de candidaturas, de momento, se hará mediante el correo vtsalamanca.
- O6. Automatización segura, verificable, de coste adicional cero y sin PC encendido.

## Inventario inicial de fuentes y estado de evidencia
| Fuente / componente | Estado registrado | Evidencia pendiente |
|---|---|---|
| Repositorio GitHub | **Comprobado**: README accesible; indica «Sin ejecuciones programadas activas» (18-10-2026) | Inventario completo de archivos, workflows, runs y artefactos |
| ATE público | **Comunicado**: funciona en GitHub, descarga/analiza PDF, huella de cambios | Revisar código y ejecuciones reales antes de declarar estable |
| ATE privado | **Historial**: se consiguió acceso o lectura al menos una vez | Repetibilidad no validada; no dar por operativo estable |
| DOCM | **Pendiente**; siguiente fuente prioritaria | Investigar acceso oficial público, formatos y filtros |
| InfoJobs privado | **Aparcado** por verificaciones y autenticación | No insistir ni eludir controles; revisar sólo si cambia el contexto |
| InfoJobs público | **Por precisar** | Identificar acceso público verificable |
| Indeed / Jobijoba | **Comunicado**: lectura pública posible | Extractores, límites y fiabilidad |
| ILUNION | **Comunicado**: acceso parcial | Alcance real |
| ACCEM / ACTIA | **Pendiente** | Canales oficiales de ofertas |
| Empléate/SEPE, CLM, Hacesfalta y otros portales | **Investigación previa, sin estado consolidado** | Inventariar resultados y evitar duplicar exploración |
| Gmail vtsalamanca | **Planificado** para seguimiento privado | Precisar filtros/datos necesarios y consentimiento para acciones |

> Ninguna fila basada sólo en conversaciones equivale a una prueba de integración estable. No inventar pruebas.

## Fases y responsables (no son entornos que deban mantenerse abiertos)

### Fase 0 — Reconciliación del historial (Chat)
- Recopilar decisiones y hallazgos de las conversaciones de Buscar-Curro y archivos existentes.
- Identificar contradicciones y puntos sin evidencias; contrastar con GitHub cuando corresponda.
- Entregable: inventario de fuentes, tareas resueltas, bloqueos y backlog sin duplicados.
- Cierre: cada fuente con estado y siguiente acción única.

### Fase 1 — Diseño funcional y fuentes (Chat)
- Priorizar DOCM, precisar categorías, alcance territorial, criterios de relevancia y salida del informe.
- Investigar canales oficiales y alternativas gratuitas; no ejecutar código.
- Entregable: especificación del módulo DOCM y backlog agrupado.
- Cierre: criterios de aceptación claros y ausencia de dependencias de pago.

### Fase 2 — Integración técnica agrupada (Codex, sólo cuando aporte ventaja)
- Revisar código existente y reutilizar módulos ATE.
- Integrar DOCM y fuentes priorizadas; normalizar datos, deduplicar y registrar errores.
- Añadir pruebas automáticas y documentación de configuración sin secretos.
- Cierre: pruebas reproducibles y cambios revisados. No lanzar sin orden expresa.

### Fase 3 — Validación operativa / interfaces (Chat primero; Work sólo si imprescindible)
- Chat + GitHub: leer resultados, revisar fallos, validar evidencias y actualizar documentación.
- Usar Work exclusivamente si una tarea requiere navegador o interacción gráfica compleja que no pueda resolverse desde Chat/conector o Codex.
- Cierre: evidencia de ejecución independiente de las fuentes críticas y coste adicional cero.

### Fase 4 — Informes y operación continua (GitHub Actions + Chat)
- GitHub recopila y conserva resultados; Chat interpreta y resume cuando se solicite o mediante automatización autorizada y disponible.
- Definir periodicidad, fallos, alertas, políticas de conservación y destinatario antes de activar.
- Cierre: ejecuciones verificables sin duplicados y con informes útiles.

## Bloque técnico agrupado BT-01 — AÚN NO AUTORIZADO PARA EJECUCIÓN
- [ ] Inventario del código, workflows y pruebas existentes en GitHub.
- [ ] Confirmar evidencia y reproducibilidad de ATE público; registrar incertidumbre en ATE privado.
- [ ] Identificar vía pública DOCM (índice, RSS, API o descarga) y límites de consulta.
- [ ] Desarrollar módulo DOCM y reglas para convocatorias, bolsas, correcciones y plazos.
- [ ] Unificar esquema de ofertas y almacenar identificadores/hash.
- [ ] Deduplicación, histórico, trazabilidad y manejo de errores.
- [ ] Agrupar pruebas unitarias, integración y ejecución independiente.
- [ ] Actualizar este documento y README con evidencias, rutas y próximos pasos.

## Registro de decisiones
- 2026-10-18: ATE público se considera funcionando según comunicación del usuario; DOCM es siguiente fuente.
- 2026-10-18: presupuesto adicional cero; ninguna ejecución técnica nueva sin permiso.
- 2026-10-18: planificar en Chat; agrupar tareas de implementación en un único bloque; Codex sólo para trabajo de programación que realmente lo requiera; Work sólo como excepción.
- 2026-10-18: usar este archivo Markdown en GitHub como memoria operativa persistente; una copia local opcional puede servir de respaldo, pero no como fuente de verdad por depender del dispositivo.
- 2026-10-18: README consultado en GitHub; consta que no hay ejecuciones programadas activas. Documento creado sin activar ninguna.

## Plantilla de avance
Fecha | Fase | Tarea | Estado (pendiente/en curso/probado/bloqueado) | Evidencia (URL/commit/run) | Problema | Próxima acción | Coste adicional

## Registro de avance — 2026-10-18: configuración local
- **Estado: comprobado mediante salida de CMD facilitada por el usuario.** Git para Windows 2.56.0.windows.2 funciona mediante `C:\Program Files\Git\cmd\git.exe`; el comando `git` a secas no se encuentra todavía en PATH.
- **Clonación terminada:** `C:\Users\Usuario\Desktop\Buscar curro` contiene copia del repositorio `vtsalamanca/Buscar-Curro`.
- **Verificación:** `git remote -v` muestra `origin` para fetch y push; `git status` indica rama `main`, actualizada con `origin/main`, y árbol de trabajo limpio.
- **Codex:** Work identificó anteriormente que el proyecto Codex apunta a esa carpeta; queda pendiente validarlo visualmente desde Codex, sin ejecutar código.
- **No realizado:** cambios en código, ejecución de workflows, actualización PATH, eliminación de carpeta antigua `buscar-curro-toledo`.
- **Próximo paso:** confirmar que Codex abre la carpeta clonada; después retomar fase DOCM siguiendo BT-01.

## Fase DOCM — investigación documental inicial (2026-10-18)
Estado: **planificación en Chat, sin ejecutar código ni workflows**.
- Confirmada la existencia de sumarios públicos del DOCM y búsqueda avanzada oficial por fecha, organismo, rango, texto y NID: https://docm.jccm.es/docm/ y https://docm.jccm.es/docm/busquedaAvanzada.do.
- NID: identificador de disposición publicado por DOCM; candidato principal para deduplicación: https://docm.jccm.es/portaldocm/verificarNID.do.
- Se observaron documentos HTML individuales oficiales en rutas verArchivoHtml.do; ejemplos publicados en 2026 permiten identificar sección II / Oposiciones y concursos, y correcciones de errores.
- **Sin verificar aún**: API pública formal, RSS disponible, límites de acceso automatizado y estabilidad del HTML; no suponer que existe API.
- Diseño propuesto: lectura de sumarios por fecha > extracción de documentos candidatos > filtros por ATE, educación, psicología, intervención social y logística > clasificación de convocatoria/corrección/resolución/plazo > deduplicación por NID > informe con enlace y fecha.
- Priorizar Toledo y alrededores sin omitir convocatorias autonómicas cuyo destino concreto todavía no figure.
- Criterios de aceptación para BT-01: recuperar ediciones y disposiciones de fechas conocidas; no duplicar NID; distinguir correcciones; mantener enlace oficial y trazas de error; cubrir días sin publicación y reintentos sin pérdida de datos.
- Próxima acción en Chat: completar especificación y contrastar contra el inventario real de código y fuentes antes de encomendar el bloque a Codex.

## Fase 0 — Reconciliación histórica ampliada (18/10/2026)
**Situación:** inventario de decisiones y fuentes recuperado; revisión exhaustiva conversación por conversación y todos los commits **no certificada**. No eliminar chats archivados.

### Fuentes históricas
- Archivo recuperado de la biblioteca: `Seguimiento_empleo_personal.md` (225 líneas; registros de búsquedas y errores hasta 17/10/2026). Contiene ofertas revisadas, controles de correo, estados de sesión, candidaturas conocidas y alternativas de acceso. Conservar como antecedente, no considerar sus vacantes vigentes sin revalidar.
- Instrucciones originales `Texto pegado.txt` («Búsqueda de empleo personal»): criterios de perfil, geografía, fuentes, deduplicación, aprobación previa de candidaturas e informes.
- GitHub: `SOURCES_STATUS.md`, `AUTH_STATUS.md`, `ate_public.py`, `test_ate_public.py`, `.github/workflows/ate-public.yml`, `README.md`. Las pruebas y sus límites figuran en los propios documentos.

### Prioridades y restricciones ACTUALIZADAS (prevalecen sobre listas antiguas)
- **Activos:** ATE Toledo/JCCM primero; psicología no sanitaria, intervención social, educación, menores y discapacidad.
- **Suspendidos desde 16/10/2026 por decisión expresa:** almacén, carretillas, logística, reparto y transporte. Guardar historial, pero NO rastrear ni recomendar hasta reactivación. Esto corrige referencias antiguas de O2 y del plan DOCM.
- Referencia territorial: Nambroca; objetivo 70 km. InfoJobs guarda +75 km porque el selector no ofrece 70 exactos.
- No enviar candidaturas ni modificar perfiles/correos sin aprobación; verificar titulación/habilitación requerida; presupuesto adicional cero.

### Evidencia técnica recuperada y alcance verdadero
| Componente | Evidencia histórica | Límite y siguiente acción |
|---|---|---|
| ATE público | Workflow `ate-public.yml`; ejecución https://github.com/vtsalamanca/Buscar-Curro/actions/runs/39152509426 ; tests y PDF público SHA-256 documentados en `SOURCES_STATUS.md` | Recuperación del PDF confirmada en esa ejecución; no extrae posiciones ni interpreta cambios, no hay programación diaria; extender, no reescribir |
| ATE privado | `AUTH_STATUS.md`: una autenticación de runner limpio y lectura privada | Repetibilidad y estado presente no demostrados; no guardar datos privados en repo |
| InfoJobs desde GitHub | HTTP 405 y verificación humana; https://github.com/vtsalamanca/Buscar-Curro/actions/runs/39127957748 | Aparcado; no repetir pruebas de CAPTCHA ni eludir barreras |
| InfoJobs perfil personal | Historial 16/10: acceso con Edge autenticado; ajustes CV, habilidad discapacidad y radio +75 km registrados | En sesiones posteriores el acceso privado volvió a solicitar identificación; conservar ambos hechos, sin presumir sesión vigente |
| DOCM | Rutas oficiales y documentos HTML consultados en investigaciones previas; también hubo timeouts en otros intentos | No hay extractor automático probado; siguiente módulo |
| GitHub local | Clonación en `C:\Users\Usuario\Desktop\Buscar curro`, `origin` correcto, rama main limpia a fecha de comprobación del usuario | Codex asociado según Work; verificar lectura de carpeta en Codex antes de desarrollar |
| GitHub Actions | En README y workflow consta ejecución por evento/manual, no schedule diario en ATE público | Revisar otros workflows antes de afirmar que todo el repositorio carece de schedule |

### Candidaturas y avisos ya conocidos: NO duplicar
- ACTIA psicología acogimiento familiar Toledo: envío documentado en Gmail de 14/10/2026; la lectura y aceptación por empresa NO constan.
- Fundación Juanjo Torrejón (07/10) y Grupo SAC (30/09): envíos documentados; respuesta no acreditada en controles disponibles.
- Acción contra el Hambre 12429 Aranjuez: oferta original revisada el 17/10; **sin candidatura enviada** en registro; requisitos y condiciones pendientes. Revalidar vigencia antes de presentarla.
- Referencias antiguas Eurofirms almacén/carretilla quedan **fuera del alcance activo**, sin borrar historial.
- Gmail segunda cuenta: cobertura incompleta; no atribuir un seguimiento actualizado que no se ejecutó.

### Correcciones de la planificación previa
- El objetivo O2 del inicio incluye logística como categoría histórica, pero está suspendida por decisión posterior. Aplicar prioridad actual arriba.
- Diseño DOCM: **no incluir logística** en filtros activos salvo reactivación expresa.
- Distinguir `verificado en ejecución histórica` de `actualmente en funcionamiento`.
- Una ejecución de diagnóstico exitosa no prueba lectura de ofertas.
- Los chats archivados permanecen como respaldo hasta inventario histórico suficiente; no garantizar que su contenido sea recuperable íntegramente por búsqueda.

### Siguiente fase
1. Terminar comprobaciones de archivos/workflows no leídos mediante inventario de repositorio, **sin volver a recorrer diagnósticos ya documentados**.
2. Preparar criterios de aceptación DOCM y tareas agrupadas BT-01 con alcance activo.
3. Reservar Codex para ese único bloque técnico y Work sólo si aparece un obstáculo que requiera interfaz.

## Fase 0 — Cierre operativo del inventario técnico (18/10/2026)
**Cierre operativo con reservas**, no una certificación de lectura exhaustiva de todas las conversaciones archivadas. Lo no acreditado permanece como pendiente, nunca como resuelto.

### Inventario verificado de componentes del repositorio
| Componente | Archivos verificados | Activación / conclusión |
|---|---|---|
| ATE fuente pública | `ate_public.py`, `test_ate_public.py`, `.github/workflows/ate-public.yml` | Workflow `workflow_dispatch` o `push` limitado a sus tres archivos; **no schedule**; test + descarga/comprobación PDF |
| ATE autenticación privada | `ate_auth.py`, `test_ate_auth.py`, `.github/workflows/ate-auth.yml` | **manual**; usa Secrets ATE, no publicar datos |
| Prueba conjunta de autenticación | `.github/workflows/auth-joint.yml` | **manual**; ATE e InfoJobs, exigencia de éxito de ambos; un fallo global no borra el posible éxito parcial ATE |
| InfoJobs autenticación | `infojobs_auth.py`, `test_infojobs_auth.py` | Acceso privado no validado desde GitHub |
| InfoJobs navegador público | `infojobs_browser_probe.py`, `.github/workflows/infojobs-browser.yml` | **manual**, sin credenciales; Chrome estándar; defensa anti-bot observada |
| InfoJobs conectividad | `infojobs_connectivity.py`, `.github/workflows/infojobs-connectivity.yml` | **manual**; sólo conectividad pública |
| Documentación | `README.md`, `AUTH_STATUS.md`, `SOURCES_STATUS.md`, `ESTADO_PROYECTO.md`, `skills/organizaciondeltrabajo/SKILL.md` | Fuente de verdad y antecedentes |

**Conclusión:** cinco workflows identificados y leídos. Ninguno contiene programación `schedule`. Sólo el workflow público de ATE tiene disparador por cambios en archivos; los cuatro restantes son manuales. No confundir `push` con revisión diaria automática.

### Contradicciones resueltas
1. «ATE público funciona» = recupera y valida documento público; **todavía no** clasifica anuncios ni emite alertas por cambios persistentes.
2. «ATE privado funciona» = constancia histórica de **una** autenticación exitosa; no implica garantía de acceso recurrente.
3. «InfoJobs perfil accesible» desde Edge local en un momento y «no accesible» desde GitHub/runner no se contradicen: entornos y momentos distintos.
4. «No hay automatizaciones» se refiere a ausencia de **programación recurrente GitHub** en estos cinco workflows; las tareas programadas de ChatGPT, si existen, se gestionan aparte y no han sido auditadas aquí.
5. «Logística» aparece en material histórico pero está **suspendida** expresamente desde 16/10; no usarla en el desarrollo DOCM activo.

### Transición a fase 1 — Diseño DOCM en Chat
- Definir descubrimiento de ediciones/disposiciones oficiales por fecha; documentar formato real sin asumir API/RSS no comprobados.
- Seleccionar secciones y palabras clave: ATE, bolsas, listas, ampliaciones, psicología no sanitaria, intervención social, protección de menores, educación y discapacidad.
- Normalizar registro: `fuente`, `nid`, `url_oficial`, `fecha_publicacion`, `organismo`, `provincia`, `tipo`, `titulo`, `plazo`, `estado`, `hash`.
- Clasificar correcciones y enlaces a resolución original; evitar falsos positivos por coincidencia de términos.
- Historial y deduplicación persistente; distinguir `sin nueva publicación` de `falló la consulta`.
- Pruebas previstas: sumario conocido, documento duplicado, corrección, día sin publicación, HTTP fallido, edición sin resultados pertinentes, anuncio autonómico sin provincia explícita y plazo no indicado.
- Antes de ejecutar BT-01, examinar exclusivamente dependencias necesarias, coste/cupo disponible y seguridad; no activar schedule ni acceso privado.

### Regla de conservación
Las conversaciones archivadas son respaldo. Está permitido archivarlas; **no recomendar su borrado definitivo** hasta comprobar que no faltan decisiones únicas. Esta fase queda cerrada a efectos de continuar el diseño, con reservas claramente enumeradas.

## Fase 1 — Casos oficiales DOCM y especificación funcional (18/10/2026)
Investigación en Chat; **no** se ha ejecutado código ni activado automatizaciones.
- Búsqueda avanzada pública: https://docm.jccm.es/portaldocm/busquedaAvanzada.do — dispone de filtros por fecha de documento/publicación, órgano, rango, NID y texto. Verificada como página pública; **no** se ha validado endpoint apto para extracción automática.
- Caso base ATE: DOCM 07/07/2026, resolución 2026/5156: https://docm.jccm.es/docm/verArchivoHtml.do?ruta=2026%2F07%2F07%2Fhtml%2F2026_5156.html&tipo=rutaDocm
- Caso corrección: DOCM 10/07/2026, 2026/5293: https://docm.jccm.es/docm/verArchivoHtml.do?ruta=2026%2F07%2F10%2Fhtml%2F2026_5293.html&tipo=rutaDocm ; nuevo anexo y plazo de diez días hábiles contado desde día siguiente a publicación; **dato histórico, no plazo vigente**.
- Caso adjudicación: DOCM 03/08/2026, 2026/5762: https://docm.jccm.es/docm/verArchivoHtml.do?ruta=2026%2F08%2F03%2Fhtml%2F2026_5762.html&tipo=rutaDocm .
- Regla funcional: agrupar 5156, 5293 y 5762 como publicaciones distintas de un proceso, conservar enlaces y NID, y clasificar propuesta, corrección y adjudicación, sin confundir ofertas de destinos de aprobados con ampliación de bolsa de suspensos.
- Diseño de extracción: buscar sumarios y candidatos por fecha; procesar sólo documentos relevantes, guardar NID y relaciones; distinguir consulta fallida, día sin boletín y boletín sin coincidencias.
- Pruebas para Codex BT-01: reconocer estos 3 documentos, fechas/tipos, relación de corrección, ausencia de duplicados, plazo expresado tal como consta sin calcular vigencia histórica, anuncio autonómico sin provincia explícita, documento no relevante y error HTTP.
- Categorías activas: ATE, psicología no sanitaria, menores, educación, discapacidad e intervención social; logística continúa suspendida.
- Pendiente antes de implementar: identificar ruta oficial estable y política técnica de acceso automatizado; comprobar si existe interfaz de consulta estructurada sin presumir API o RSS.

## Fase 1 — Alternativa de captura DOCM (18/10/2026)
- Descubrimiento confirmado en página oficial indexada: **Servicio gratuito de alertas del DOCM** https://docm.jccm.es/portaldocm/solicitarAltaAlertas.do . Describe envío diario por correo según temas elegidos y opción **Empleo público**, con confirmación por correo. No se ha solicitado alta ni consentimiento. La entrega no está garantizada por el propio servicio.
- Búsqueda avanzada oficial https://docm.jccm.es/portaldocm/busquedaAvanzada.do : filtros por fecha de publicación, NID, tipo sumario/contenido y otros; páginas accesibles en índice, pero la apertura directa dio timeout en esta comprobación. No inferir una API estable.
- **Orden de preferencia propuesto:** 1) alertas oficiales como señal gratuita complementaria mediante Gmail autorizado; 2) consulta pública de ediciones/documentos DOCM con extractor cuando se confirme método estable; 3) cotejar ambas vías para detectar omisiones.
- Un sistema basado solo en alertas no garantiza cobertura histórica, independencia del correo, captación de correcciones o entrega diaria; el extractor sigue justificado para completitud y validación.
- Antes de implementar: comprobar contenido y opciones reales del correo de alerta y confirmación, con consentimiento del usuario; definir ingesta idempotente por identificador NID, fecha/enlace y registro de ausencia/fallos.
- No crear cuentas, activar suscripciones, iniciar código ni workflows en esta fase.

## Fase 1 — Decisión de arquitectura DOCM (18/10/2026)
**Resultado de comparación documental**. Sin ejecución de código, altas en alertas ni workflows.

| Vía | Ventajas | Riesgos/limitaciones | Decisión |
|---|---|---|---|
| Alertas DOCM por correo | Oficial y gratuita; selección de Empleo público y aviso diario; confirmación por email | No garantiza entrega; depende del correo y los criterios configurados; no cubre por sí sola histórico ni garantiza clasificación fina | **Complementaria**, activación sólo con consentimiento del usuario |
| Búsqueda avanzada y consulta web pública | Filtros por fecha publicación, NID, organismo, texto, sumario/contenido; enlaces oficiales | Interfaz HTML, parámetros de automatización aún no comprobados; no presumir API/RSS estable; vigilar fallos | **Fuente primaria propuesta**, pendiente validar método técnicamente |
| ELI / NID | Identificador y rutas de disposiciones útiles para trazabilidad | NID identifica documento, no necesariamente el proceso administrativo; ELI no es necesariamente índice completo de todas las ofertas | Usar como identificador documental y vincular correcciones por contenido |

Fuentes oficiales verificadas: https://docm.jccm.es/portaldocm/solicitarAltaAlertas.do ; https://docm.jccm.es/docm/busquedaAvanzada.do ; https://docm.jccm.es/portaldocm/verificarNID.do .
Servicio de alertas: gratuito, diario y configurable; solicita consentimiento y confirmación por email; no se tramitó.

### Diseño funcional acordado (para paquete técnico BT-01, aún sin autorización de ejecución)
1. Construir un lector público de ediciones y disposiciones oficiales, con lectura por rango de fechas y control de errores.
2. Identificar por NID y enlace canónico, registrar fecha, título, organismo, ámbito, tipo de acto y relación con otras disposiciones.
3. Clasificar ATE, bolsa/ampliación, oposiciones, psicología no sanitaria, protección de menores, discapacidad, educación e intervención social. Logística **excluida** del alcance activo.
4. Distinguir resolución, corrección, convocatoria, adjudicación, modificación y apertura/cierre de plazos; no calcular automáticamente que los plazos están abiertos sin regla validada.
5. Persistir NID/documentos vistos y eventos de cambio; no duplicar resultados aunque cambie el enlace; conservar histórico.
6. Informar sólo novedades relevantes y mantener un informe de fallos separado. «Sin nuevos anuncios» solo si hubo consulta exitosa.
7. Habilitar opcionalmente contraste con correos de alertas oficiales cuando el usuario autorice el alta y el canal esté disponible. No requerir Gmail para que funcione la fuente primaria.
8. Pruebas con documentos históricos ATE 07/07, 10/07 y 03/08/2026, documentos no relevantes, fallos/redirecciones, ausencia de sumario, fechas sin publicación, duplicados, correcciones y filtrado autonómico.
9. La programación recurrente y distribución del informe quedan **fuera del BT-01 inicial** hasta pruebas y autorización; no crear workflow de ejecución diaria por inercia.

### Siguiente paso
Preparar instrucción única para Codex tras validar coste/cupo y método de lectura pública; conservar pruebas actuales ATE y no tocar autenticaciones privadas. Fase 1 funcional cerrada, **validación técnica del protocolo DOCM pendiente**.

## Fase previa a programación — Auditoría de fuentes, lote 1 (18/10/2026)
Se recuperaron resultados anteriores antes de ampliar fuentes. No hubo ejecución de scripts, Work, Codex ni Actions. **Prueba web en Chat no equivale a prueba automática en runner**.

| Fuente | URL oficial / evidencia de consulta | Estado de acceso público | Automatización | Acción posterior |
|---|---|---|---|---|
| ATE JCCM público | https://github.com/vtsalamanca/Buscar-Curro/actions/runs/39152509426 | Verificado históricamente | Prueba runner positiva, sólo PDF/hash | Reutilizar código, integrar cambios y textos |
| ATE privado | AUTH_STATUS.md | Autenticación una vez | No repetible verificado | No repetir sin necesidad, sin secretos en informes |
| DOCM | https://docm.jccm.es/docm/busquedaAvanzada.do | Formulario y filtros públicos identificados | No verificado | Ensayo técnico acotado en BT-01 |
| BOP Toledo | https://bop.diputoledo.es/webEbop/ebop.jsp | Buscador público por texto, anunciante, fechas y paginación; documentos anteriores a 01/07/2009 no indexados | No verificado | Confirmar URLs de detalle, paginación y cambios |
| BOE / Mi BOE | https://boe.es/alertas/ ; https://administracion.gob.es/empleopublico/guia-buscador | Alertas gratuitas oficiales; guía de convocatorias accesible; RSS anunciado | No verificado | Priorizar vías estructuradas oficiales y evitar duplicar DOCM/BOP |
| Empléate | https://empleate.gob.es/empleo/index_nojs.html?JAVASCRIPTSTATUS=NONE | Portada alternativa accesible, búsqueda visible; historial de búsqueda real parcial | No verificado | Revisar salida y criterios sin inferir que catálogo completo es accesible |
| Centro Trama | https://www.trama.org/empleo/ | Catálogo y fichas originales públicos con fechas de cierre; algunos anuncios vencidos siguen visibles | No verificado | Alto potencial para extractor HTML y descarte por fecha, requisitos de titulación |
| ACCEM | Seguimiento_empleo_personal.md; catálogo 19 revisado históricamente | Parcial, no todas las vías | No verificado | No repetir recorrido previo sin cambios |
| Cruz Roja | Seguimiento_empleo_personal.md; https://cruzroja.epreselec.com/Ofertas/Ofertas.aspx | Catálogo con filtros revisado históricamente | No verificado | Revisar parámetros de acceso y requisitos |
| InfoJobs | AUTH_STATUS.md; HTTP 405/desafío humano en runner | Perfil en Edge local históricamente, sin acceso runner | Bloqueado | Aparcado; usar email autorizado, nunca eludir verificación |

### Decisiones del lote
- ATE público continúa como fuente funcional parcial; no reescribir.
- BOE y BOP Toledo se incorporan expresamente al inventario (además de DOCM).
- Centro Trama pasa a prioridad alta de empleo social, por fichas públicas estructuradas.
- Empléate se mantiene parcial, no atribuir cobertura total por cargar portada.
- Alertas oficiales DOCM y BOE pueden complementar captación con consentimiento; no están activadas.
- Fuentes pendientes siguientes: empleo autonómico/local, ayuntamientos, ACTIA, ILUNION/Inserta, entidades restantes, Indeed, Jobijoba, LinkedIn y correo; para cada una registrar método y límites.
- **Puerta de fase:** las pruebas de automatización se agruparán por familias en Codex sólo después de completar inventario y priorización; no se exigirán credenciales ni se reabrirán pruebas bloqueadas innecesariamente.

## Auditoría de fuentes — Lote 2 y agrupación siguiente (18/10/2026)
Comprobación web pública puntual; las cifras de anuncios son dinámicas y no constituyen prueba de lectura automatizada ni vigencia futura.
- **Empleo CLM:** https://empleo.castillalamancha.es/ ; listado público con denominación, municipio, contrato, jornada, salario, filtros por provincia/municipio/CNO. Existen valores posiblemente anómalos; exigir validación y origen por oferta. **Acceso público verificado; runner pendiente.**
- **Bolsas laborales JCCM:** https://empleopublico.castillalamancha.es/bolsas/personal-laboral ; categorías y subgrupos disponibles. **Acceso público verificado; runner parcial ATE solamente.**
- **ATE bolsa directa:** https://empleopublico.castillalamancha.es/bolsas/personal-laboral/grupo-iii-auxiliar-tecnico-educativo ; página con modificación 06/10/2026, provincias y PDFs. La fecha de actualización de la página NO significa necesariamente un listado nuevo de Toledo.
- **ATE proceso selectivo:** https://empleopublico.castillalamancha.es/procesos-selectivos/abiertos/turno-libre/2023-2024-grupo-iii-auxiliar-tecnico-educativo-turno-libre ; documentos de adjudicación, correcciones y destinos, **proceso diferente de ampliación de bolsa de suspensos**.
- **JCCM últimas modificaciones:** https://empleopublico.castillalamancha.es/ultimas-modificaciones ; útil como fuente incremental, pero filtrar por entidad y tipo y no confundir movimientos de otros cuerpos.
- **Educación social JCCM:** https://empleopublico.castillalamancha.es/bolsas/personal-funcionario/cuerpo-tecnico-escala-sociosanitaria-educacion-social ; página pública de bolsas por provincia, elegibilidad específica por determinar.
- **Centro Trama:** https://www.trama.org/empleo/ catalogo accesible; incluye algunas fichas con fecha de cierre pasada pese a aparecer en listado. La oferta no es automáticamente elegible por afinidad; comprobar requisitos formativos.
- **ACTIA/ILUNION/ACCEM/Inserta/otros:** usar inventario histórico de Seguimiento_empleo_personal.md antes de nuevas consultas; pendientes validación técnica o cobertura selectiva.
- **Indeed/Jobijoba/LinkedIn/InfoJobs:** acceso parcial documentado; no asumir API libre ni acceso sin interacción. InfoJobs privado aparcado.
- **Gmail:** seguimiento de candidaturas separado del rastreo de vacantes; requiere conexión autorizada y no se considera automatización GitHub.
 
### Agrupación funcional y técnica por familias
A) **Administraciones/boletines:** ATE público, JCCM últimas modificaciones, DOCM, BOP Toledo, BOE/Punto de Acceso General.
B) **Intermediación empleo:** Empleo CLM, Empléate y ayuntamientos; revisar filtros, referencias y paginación.
C) **Entidades sociales:** Centro Trama, ACCEM, ACTIA, Cruz Roja, ILUNION, Inserta/Portalento, Save the Children y otras. Empezar con catálogos públicos estructurados.
D) **Portales/privado:** Indeed, Jobijoba, LinkedIn e InfoJobs: tratamiento de acceso limitado, sin bypass de verificación.
E) **Correspondencia y candidaturas:** Gmail, sin enviar ni cambiar estados sin orden del usuario.

**Puerta de decisión:** primero completar tabla de métodos y limitaciones a partir de antecedentes por familia; después enviar un único encargo Codex por paquete viables, con pruebas y alcance finito. No bloquear la totalidad por fuentes que exigen login o están aparcadas. No activar workflows programados antes de pruebas.

## Auditoría de fuentes — Lote 3 / continuidad sin pausa (18/10/2026)
Se prosiguió dentro del mismo encargo, sin pedir un nuevo «sigue», sin ejecutar código ni gastar servicios tarificados. Se utilizaron fuentes públicas y antecedentes.

| Fuente | Evidencia pública revisada | Alcance y límites | Prioridad |
|---|---|---|---|
| Ayuntamiento Toledo | https://www.toledo.es/el-ayuntamiento/empleo-publico/ | Convocatorias y bolsas con fechas de solicitud y bases. Ejemplo histórico: bolsa Educador/a Social plazo 21–31/08/2026, bolsa Educador/a-Cuidador/a de centro de atención VVG, resolución 22/09/2026. **Listado público verificado, extracción runner pendiente.** | Alta |
| Diputación Toledo | https://www.diputoledo.es/global/50/304/4664 | Secciones de empleo público, OPE 2026, bolsas y solicitudes; fichas por categorías y varios documentos por proceso. **Acceso público verificado, automatización pendiente.** | Alta |
| ILUNION | https://empleo.ilunion.com/go/ILUNION-VIDASENIOR/8683602/ | Catálogo y referencias publicadas, ID de vacante (p.ej. 38668 Sonseca) y fecha; fichas con titulación exigida. Anuncio 38668 requiere FP sociosanitaria, no suponer equivalencia con Psicología. **Acceso público verificado, automatización pendiente.** | Media |
| ACTIA | https://www.actiasocial.org/ubicacion.html ; Hacesfalta en registros anteriores | Sitio institucional aporta servicios y contacto, pero no demuestra catálogo de vacantes. Consulta de Hacesfalta y candidatura ACTIA anterior ya registrada: no repetir envío. **Fuente de empleo parcial.** | Media |
| Inserta/Portalento | https://www.portalento.es/Candidatos/Ofertas/Default.aspx (histórico) | Filtro Toledo sin resultados en prueba previa; no es evidencia de ausencia general. Comprobar sólo con nuevo alcance justificado. | Media |
| ACCEM | Historial: catálogo 19 resultados en dos páginas | No repetir recorrido sin cambio o fuente nueva. | Media |
| Cruz Roja | https://cruzroja.epreselec.com/Ofertas/Ofertas.aspx (histórico) | Catálogos Toledo/Madrid revisados parcialmente; salarios/requisitos deben obtenerse de ficha. | Media |
| Portales dinámicos (Indeed/Jobijoba/LinkedIn) | Historial `Seguimiento_empleo_personal.md` | Lectura parcial y caducidades; no atribuir automatización ni API. | Baja hasta pruebas focalizadas |

**Reglas de selección:** verificar fecha de publicación y plazo, comprobar títulos habilitantes obligatorios, distinguir bolsa de vacante, conservar ID/enlace original, deduplicar entre DOCM/BOP/ayuntamientos/empleador. No rastrear logística suspendida. Priorizar fuentes oficiales y catálogos de organizaciones con fichas completas. 

**Siguiente paquete lógico de auditoría (sin ejecutar código):** mapear cobertura de otros ayuntamientos del entorno y completar límites de ACCEM/Cruz Roja/Trama y Empléate; la prueba de lectura automatizada por runners pertenece al bloque Codex ya agrupado y no debe confundirse con comprobaciones web.

## Auditoría lote 4 — fuentes municipales, trazabilidad y deduplicación (18/10/2026)
Comprobación pública por lectura/búsqueda web, **no prueba de GitHub Actions**. No se ejecutó código, se activaron workflows ni se enviaron candidaturas.

| Fuente | URL pública y observación | Estado automatización |
|---|---|---|
| Nambroca sede | https://nambroca.sedelectronica.es/info.0 ; tablón con anuncios de procesos, listados y subsanaciones (ej. mantenimiento 06/10) | Pendiente |
| Aranjuez empleo público | https://www.aranjuez.es/transparencia/empleo-publico/documentacion-importante/ ; documentación por procesos; https://www.aranjuez.es/transparencia/empleo-publico/trabajador-social/ registra bases, corrección, BOCM, BOE y plazo histórico | Pendiente |
| Sonseca sede | https://sonseca.sedelectronica.es/info.0 ; sección de empleo público y tablón | Pendiente |
| Bargas empleo | https://www.bargas.es/empleo/ ; listado de ofertas y noticias, muchas antiguas: no equiparar fecha del índice con vigencia | Pendiente |
| Toledo Ayuntamiento | https://www.toledo.es/el-ayuntamiento/empleo-publico/ ; acceso libre, bolsas y plazos en fichas | Pendiente |
| Centro Trama | https://www.trama.org/empleo/ ; catálogo público y fichas por id `oferta.php?id=...`, fecha de cierre y requisitos; aparecen fichas con plazos pasados | Pendiente |

### Ejemplo de deduplicación jurídica entre boletines
- Illescas, dos plazas de Trabajador/a Social: BOE https://www.boe.es/diario_boe/txt.php?id=BOE-A-2026-7237 menciona bases BOP Toledo n.º 16 del 27/01/2026 y anuncio BOE 30/03/2026. El registro debe identificar un **proceso** con **varios actos/publicaciones**. No fusionar los documentos en una sola publicación, ni generar varias novedades de la misma vacante.
- Aranjuez, Trabajador Social: ficha municipal https://www.aranjuez.es/transparencia/empleo-publico/trabajador-social/ lista bases, corrección, BOCM, BOE y plazo histórico 25/06–22/07/2026; demuestra necesidad de enlazar actos.
- Casos de prueba BT-01: dos boletines sobre mismo proceso, corrección que modifica base/plazo, convocatoria vencida aún indexada, oferta privada sin plazo, anuncio de plaza fuera de sector activo.

### Decisión de arquitectura
Definir objetos `source_document` (NID/BOE-ID/URL/fecha/organismo) y `selection_process` (organismo, categoría, referencia, municipios, historial actos) con relación muchos-a-uno, conservando trazabilidad y evitando falsas novedades. No inferir plazo abierto por existencia de enlace.

## Auditoría lote 5 — contrastes finales de fuentes públicas (18/10/2026)
- **Empléate (SEPE):** https://empleate.gob.es/empleo/index_nojs.html?JAVASCRIPTSTATUS=NONE : portada/búsqueda públicas accesibles. Las cifras de su portada cambian y NO prueban cobertura de resultados filtrados ni API pública. Estado **parcial**, runner pendiente.
- **Diputación Toledo:** https://www.diputoledo.es/global/50/304/6699/destacados-rrhh : destacados cronológicos con fecha y tipo; https://www.diputoledo.es/global/50/1450/5716/opcion : expedientes y actos múltiples por plaza. Estado **público accesible**, extracción/paginación runner pendientes.
- **Centro Trama:** https://www.trama.org/empleo/ lista activa, pero conserva entradas con fechas de cierre ya pasadas. Fichas individuales https://www.trama.org/empleo/oferta.php?id=1131 y otras contienen requisitos de grado/FP obligatorios; no equiparar Psicología con FP Integración Social. Estado **público accesible**, runner pendiente.
- **ACCEM:** la página https://www.accem.es/programas contiene actividades y servicios, **no** es un catálogo de empleo. Conservar el catálogo empleador históricamente revisado en InfoJobs (19 fichas) como acceso parcial, sin inventar nueva fuente estructurada.
- **Inserta/Portalento:** https://www.portalento.es/Candidatos/Ofertas/Default.aspx revisada históricamente con filtros; requerimientos personales para acceso a programas no deben presumirse. Estado parcial, no declarar ausencia total por resultados vacíos en Toledo.
- **Bargas:** https://www.bargas.es/empleo/ y https://www.bargas.es/empleo/ofertas-de-empleo/ mezclan ofertas recientes/antiguas e información formativa; clasificar antes de alertar.
- **Nambroca:** https://nambroca.sedelectronica.es/info.0 tablón reciente, incluye anuncios de mantenimiento y otros puestos ajenos a los sectores activos. Seguir las novedades municipales con filtrado, no asumir relevancia.
- **Aranjuez:** https://www.aranjuez.es/transparencia/empleo-publico/trabajador-social/ muestra secuencia bases-corrección-BOCM-BOE y plazo histórico, caso ideal para prueba de vinculación de actos.
- **Portales dinámicos/privados:** Indeed, Jobijoba, LinkedIn: cobertura parcial ya documentada; InfoJobs automatización desde runner bloqueada por comprobación humana; no reiniciar diagnósticos idénticos.
- **Cruz Roja, ILUNION y ACTIA:** mantener rutas documentadas en lotes previos; los bloqueos ocasionales de navegador no equivalen a ausencia de puestos.
- **Pendientes específicos sin bloqueo para planificación:** boletín BOCM para Aranjuez/Madrid; bolsas y tablones de Illescas y otros municipios (seleccionar por prioridad); cobertura histórica efectiva por familia; verificación automatizada desde runner en Codex.

### Puerta de auditoría y paquete técnico recomendado
**Inventario funcional suficiente para pasar al diseño técnico agrupado**, con fuentes no verificadas automáticamente clasificadas como tales. No afirmar acceso automático por mera lectura en Chat.

**BT-01A (Codex, propuesta, NO ejecutado):** pruebas de viabilidad runner exclusivamente públicas y sin login, agrupadas por familias A (DOCM, BOE, BOP, JCCM) y B (Empleo CLM, Empléate, Toledo/Nambroca/Aranjuez) y C (Trama, ILUNION, Cruz Roja, ACCEM cuando enlace directo disponible); guardar códigos de estado, estructura, ejemplo sanitizado, clasificación y errores. Reutilizar ATE público; prohibido activar schedule, rellenar credenciales o modificar datos del usuario. Separar prueba de viabilidad de la programación definitiva.
**BT-01B (Codex, después de validar fuentes):** implementar extractores viables con estado persistente, deduplicación por proceso y acto, filtros de elegibilidad, pruebas de regresión y reportes. Bloqueadas se registran, no se fuerzan.
**Fase operativa posterior:** elección de periodicidad, alertas, correo y costes reales para aprobación expresa; sin activación implícita.

## BT-01A — resultado técnico agrupado (18/10/2026)

**Estado: probado y documentado; BT-01B no iniciado.** Autorización recibida para ejecutar exclusivamente BT-01A y comprobar las fuentes públicas desde GitHub Actions, con coste adicional cero.

- Código: `source_viability.py`, `test_source_viability.py` y `.github/workflows/bt01a-source-viability.yml`; commits `feb84c0` y corrección `67cbea0`.
- Seguridad/alcance: workflow exclusivamente manual (`workflow_dispatch`), runner estándar, `contents: read`, timeout global de 7 minutos, 15 segundos y 1 MiB por fuente, un intento, metadatos públicos sanitizados, sin secretos o autenticaciones. No se modificó `ate_public.py` ni se ejecutaron ATE privado o InfoJobs autenticado.
- Verificación válida: https://github.com/vtsalamanca/Buscar-Curro/actions/runs/39163691686 ; nueve tests superados, todos los pasos correctos, artefacto ID `12149183682` con retención de 7 días y SHA-256 ZIP `86795d842a8c188039de4b5e1d064cab0be518eec9b66e4ccfc7f704c73e36c5`.
- **Viables para estudiar en BT-01B:** DOCM, BOE documental, BOP Toledo, JCCM últimas modificaciones, Ayuntamiento de Aranjuez e ILUNION VidaSénior (HTTP 200 con estructura/enlaces relevantes detectados).
- **Parciales:** Empleo CLM, Ayuntamiento de Toledo, Centro Trama y Cruz Roja. Respondieron HTTP 200, pero la prueba estática no confirmó enlaces de resultados o detectó señal de login; necesitan una prueba focalizada de catálogo/fichas antes de programar conectores.
- **Bloqueadas en este run:** Empléate (`network_error`) y sede de Nambroca (`HTTPError:302`). No se reintentaron ni forzaron.
- **No probada:** ACCEM, porque no se validó una URL oficial directa de vacantes y su página de programas no es un catálogo.
- La primera ejecución https://github.com/vtsalamanca/Buscar-Curro/actions/runs/39163408797 se conserva como diagnóstico **descartado para la matriz**: una coincidencia demasiado amplia interpretaba `meta robots` como reto humano. Se corrigió y se añadió test de regresión antes de la ejecución válida.
- Limitación transversal: `verificada_desde_runner` demuestra acceso público y enlaces relevantes en esa fecha y runner; no prueba todavía paginación, cobertura, vigencia, extracción semántica, deduplicación ni estabilidad futura.
- Avisos de mantenimiento: actions basadas en Node.js 20 fueron forzadas a Node.js 24 y GitHub anunció migración de `ubuntu-latest`; no afectaron el resultado, pero deberán revisarse antes de una fase operativa.

**Puerta siguiente:** detenerse aquí para revisión del usuario. No comenzar BT-01B, no añadir conectores definitivos, no activar cron ni notificaciones hasta nueva autorización.

## BT-01B — implementación y verificación agrupada (18/10/2026)

**Estado: desarrollado, publicado y verificado; pendiente de revisión funcional antes de cualquier fase operativa.** La autorización posterior permitió ejecutar BT-01B sin ampliar el alcance a autenticaciones, candidaturas, cron o notificaciones.

- Implementación: `employment_core.py`, `public_connectors.py`, `run_public_sources.py`, tests y workflow manual `.github/workflows/bt01b-public-sources.yml`.
- Funciones: modelo común, filtros de categorías activas y logística suspendida, fechas/plazos conservadores, requisitos presentes en texto, identidad por fuente, hash, relación de actos, estado JSON persistente, detección de nuevos/cambiados, deduplicación y separación de error frente a cero resultados.
- Conectores con documentos reales desde runner: DOCM 3, BOE 1, JCCM 2, Ayuntamiento de Toledo 2, Aranjuez 1, Trama 10 e ILUNION 10. Son documentos candidatos; plazo desconocido, distancia o titulación pendiente impiden tratarlos automáticamente como recomendación.
- Acceso parcial sin documentos extraíbles: BOP Toledo 0 (formulario/paginación no implementados), Empleo CLM 0 (catálogo no visible estáticamente) y Cruz Roja 0 (detalle con `HTTPError:302`). No se forzaron ni se ocultaron como “sin novedades”.
- Verificación válida: https://github.com/vtsalamanca/Buscar-Curro/actions/runs/39165959658, commit `b45f02e`, 20 tests en Actions, todos los pasos correctos; artefacto ID `12150139921`, SHA-256 `45909783b7b9d0bb5cff28c6422569263e67c80c1b4465a8fe0ab2db3955c68e`, retención 7 días. Suite local completa: 31 tests correctos, incluidas regresiones ATE.
- Commits BT-01B: `fa6ac15` (pipeline), `aa1ba83` (evidencias y extracción), `e96cb81` (navegación JCCM) y `b45f02e` (filtros finales).
- Las ejecuciones `39165252983`, `39165510317` y `39165713985` son diagnósticas; revelaron y permitieron corregir falsos positivos antes de declarar el run final.
- Coste/seguridad: solo biblioteca estándar de Python y GitHub-hosted runner estándar del repositorio público; sin dependencias tarificadas, secrets, cookies ni datos privados. El código ATE existente no fue modificado.
- Limitaciones abiertas: descubrimiento exhaustivo DOCM/BOE, consulta real del formulario BOP, catálogo dinámico Empleo CLM, redirecciones de Cruz Roja, paginación, cálculo geográfico de 70 km y validación automática de titulaciones. Hasta resolverlas, los documentos son candidatos auditables, no recomendaciones ni ofertas confirmadas como vigentes.

**Puerta siguiente:** revisar estos resultados con el usuario. No activar frecuencia, notificaciones ni integraciones privadas; cualquier siguiente bloque requiere una decisión posterior.
