---
name: organizaciondeltrabajo
description: Protocolo reutilizable para organizar proyectos, recuperar decisiones previas, reducir repeticiones y minimizar tiempo, créditos y gasto adicional. Aplicar al planificar, ejecutar, revisar o retomar tareas.
version: 0.1.0
---

# &organizaciondeltrabajo

## Misión
Conseguir resultados fiables y verificables con el mínimo gasto razonable de tiempo, herramientas, cuotas y créditos. Aprender de cada intervención y actualizar este protocolo de manera incremental. Presupuesto adicional por defecto: **0 €**.

## Activación
Aplicar cuando el usuario invoque `&organizaciondeltrabajo` y como metodología de referencia cuando organice proyectos. Esta carpeta contiene el **texto fuente de la skill**: no implica que esté instalada o activada automáticamente como plugin de ChatGPT.

## Reglas prioritarias
1. No utilizar APIs, plugins o servicios de pago por uso, aunque tengan crédito promocional, sin informar de tarifa, coste y saldo conocidos y obtener autorización expresa. Si no se puede verificar el coste, no ejecutar.
2. Preferir Chat para conversación, investigación y planificación. Usar Codex para cambios de código, depuración o pruebas que lo justifiquen; Work para navegación/interacción compleja que no pueda abordarse razonablemente con opciones de menor coste. No cambiar de modo sin intervención del usuario.
3. Antes de empezar, consultar el estado maestro del proyecto, archivos/repositorio y resultados previos; evitar repetir investigaciones y pruebas realizadas. No presentar resúmenes de conversaciones como evidencia técnica.
4. Priorizar herramientas incluidas, gratuitas y ya conectadas; revisar habilidades disponibles antes de añadir nuevas dependencias.
5. Agrupar modificaciones, pruebas y despliegues en bloques técnicos; no fragmentar intervenciones costosas. Preservar lo que funciona.
6. Nunca afirmar éxito sin evidencia. Registrar origen, fecha, versión, estado y condiciones de cada prueba. Ante un fallo: diagnosticar antes de repetir.
7. No realizar acciones externas sensibles o irreversibles sin la autorización requerida; no exponer secretos en documentación.
8. La optimización de cuotas no debe comprometer fiabilidad, legalidad, seguridad ni verificabilidad.

## Proceso de trabajo
### A. Recuperar contexto (Chat)
- Identificar objetivo, restricciones, fuentes, estado y decisiones anteriores.
- Consultar `ESTADO_PROYECTO.md` u otro registro maestro y verificar contra repositorio/fuentes cuando sea material.
- Marcar cada dato: **verificado**, **comunicado**, **hipótesis**, **pendiente**, **bloqueado** o **descartado**.
- Resolver contradicciones antes de repetir pasos.

### B. Planificar (Chat)
- Escribir objetivo medible, entregable y criterios de aceptación.
- Desglosar dependencias y ordenar tareas, sin saltarse las bloqueantes.
- Asignar cada tarea al entorno de menor coste efectivo: Chat, conector, Codex o Work.
- Agrupar tareas técnicas compatibles en un único bloque y estimar riesgos/coste adicional.
- Señalar acciones que requieren autorización.

### C. Ejecutar con control (entorno apropiado)
- Realizar solo tareas autorizadas. Verificar antes de modificar archivos existentes.
- Reutilizar código, sesiones y hallazgos válidos; no disparar ejecuciones duplicadas.
- Mantener cambios mínimos y reversibles, pruebas reproducibles y diagnóstico de errores.
- Trabajar sin servicios de pago por uso no autorizados.

### D. Verificar y documentar (Chat + repositorio)
- Comprobar el entregable contra los criterios de aceptación.
- Guardar prueba o vínculo a commit, ejecución, archivo, fuente o decisión.
- Actualizar el registro maestro con hechos, bloqueos y próxima acción.
- Cerrar una fase solo con evidencias; no confundir `creado` con `probado`.

### E. Aprendizaje y mejora continua
- Tras detectar una repetición, error o pérdida de contexto, añadir una causa y una mejora concreta.
- Comparar coste/esfuerzo previsto frente a realizado cuando haya datos.
- Proponer versiones incrementales de la skill, con historial de cambios; no cambiar criterios esenciales silenciosamente.
- Revisar de forma periódica si una regla reduce realmente tiempo o créditos.

## Regla de asignación de entornos
| Entorno | Sí | No |
|---|---|---|
| Chat | Definir tareas, buscar y resumir, usar conectores disponibles, analizar resultados, actualizar documentos si posible | Recurrir por rutina a Work o Codex |
| Codex | Programación, refactor, tests, diagnóstico técnico agrupado | Consultas sencillas, redacción o investigación general |
| Work | Interacciones complejas en navegador/escritorio, flujos gráficos no accesibles por conectores o código | Seguimiento documental que pueda hacerse desde Chat/GitHub |
| GitHub | Fuente de verdad, código, documentación, histórico, pruebas y automatizaciones autorizadas | Almacenar credenciales o asumir que un workflow está activo sin comprobarlo |

## Registro mínimo de cada tarea
`ID | Proyecto | Objetivo | Responsable/entorno | Estado | Evidencia | Dependencias | Coste autorizado | Siguiente paso`

Estados: `pendiente`, `planificado`, `en curso`, `bloqueado`, `probado`, `cerrado`. Escribir quién verificó y cuándo.

## Condiciones para comenzar un bloque técnico
- Objetivo claro y criterios de salida;
- código/recursos previos identificados;
- dependencias ordenadas;
- alternativas gratuitas consideradas;
- coste adicional cero o autorización expresa;
- plan de pruebas y reversión.

## Aplicación inicial: Buscar-Curro
Fuente de verdad: `ESTADO_PROYECTO.md` en el repositorio `vtsalamanca/Buscar-Curro`. ATE público comunicado como operativo, DOCM siguiente integración pendiente. Agrupar futuras tareas en BT-01. No activar GitHub Actions ni ejecutar código sin instrucción.

## Cambios de la skill
- **0.1.0 — 2026-10-18:** primera versión; control de costes, continuidad, fases, evidencias, reparto Chat/Codex/Work y mejora iterativa.
