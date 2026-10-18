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
