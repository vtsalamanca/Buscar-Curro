# Buscar Curro — BC-08: resultados para ChatGPT y ejecución diaria

## Alcance y presupuesto
- Ejecución diaria a las **06:17 Europe/Madrid**, también manual, y primera verificación por push del propio workflow: `.github/workflows/daily-search.yml`.
- Sólo runner estándar `ubuntu-24.04` en repositorio público, biblioteca estándar, sin pagos, instalación de servicios, cache ni artefactos.
- Se ejecutan fuentes ETT públicas, portales públicos acotados, BOE (7 días), DOCM (último diario) y monitor de huella del PDF ATE Toledo. **No es cobertura exhaustiva** de BOP, Empleo CLM ni páginas privadas.
- Las búsquedas registran errores y cobertura incompleta, no afirman que «no hay ofertas» tras un fallo.

## Rama de resultados
- Rama exclusiva: `buscar-curro-resultados`. Fuente de lectura en `notices/latest.json`, histórico reducido en `notices/states/*.json`.
- **La rama es pública.** Se proyecta sólo un subconjunto de documentos profesionales públicos (identificador, huella, título, URL HTTPS sin credenciales, fecha, localidad y clasificación) y cola de enlaces de anuncios públicos. Nunca se guarda allí el estado bruto, texto íntegro, datos de solicitantes del PDF, credenciales o candidaturas privadas.
- Arranque de ETT: intenta recuperar una única vez el artefacto de BC-03 en área temporal y **sanearlo antes de guardarlo en la rama pública**. Si ha caducado, empieza sin la cola heredada. Cualquier fallo de lectura del estado persistente detiene el trabajo sin borrar dicho estado.
- Los resultados diarios etiquetan `verified_offer:false`: son candidatos preliminares, no afirmaciones de vacante vigente, requisitos cumplidos ni distancia de carretera. Cada aviso debe validar la ficha oficial y el plazo.
- El cambio de huella del PDF ATE **no revela** contenidos ni acredita un llamamiento. Sólo dispara una revisión oficial.
- Git conserva versiones anteriores sin depender de artefactos caducables; conviene tener copia externa del histórico público.

## Enlace y avisos
- https://github.com/vtsalamanca/Buscar-Curro/blob/buscar-curro-resultados/notices/latest.json
- https://raw.githubusercontent.com/vtsalamanca/Buscar-Curro/buscar-curro-resultados/notices/latest.json
- Las tareas ya creadas en ChatGPT han de leer el JSON, comprobar `generated_at`, `overall_status`, `events` y `source_failures`. No confundir una tarea de ChatGPT activada con un canal de entrega extremo a extremo probado.
- Cuando haya novedades, consultar fuente, vigencia, ubicación y requisitos antes de notificar; excluir almacén/logística y titulaciones no disponibles.
- Domingo: resumen semanal aun sin nuevas vacantes, dejando constancia de fallos y última ejecución.

## Riesgos y reversión
- Un workflow programado de GitHub puede retrasarse o desactivarse por inactividad. Alertar si `generated_at` envejece más de ~36 h; una ausencia de fecha no implica ausencia de ofertas.
- Permisos de la tarea: `contents:write` exclusivamente para publicar sobre rama de resultados, `actions:read` para rescatar el artefacto histórico. No almacena tokens.
- GitHub documenta ejecutores estándar gratuitos en repositorios públicos. **No se ha podido inspeccionar la configuración privada de facturación de la cuenta desde este conector**; se ha evitado el almacenamiento de artefactos, runners grandes o servicios de pago.
- Reversión: Actions → «Buscar Curro — consulta diaria pública» → Disable workflow; conservar ambas ramas para auditoría.
- Hasta la primera ejecución remota real y lectura desde ChatGPT, el sistema está *integrado en código* pero **no verificado de extremo a extremo**.
