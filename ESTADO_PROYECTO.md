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
