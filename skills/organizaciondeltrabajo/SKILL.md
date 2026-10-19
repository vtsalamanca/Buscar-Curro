---
name: organizaciondeltrabajo
description: Protocolo reutilizable para organizar proyectos, recuperar decisiones previas, reducir repeticiones y minimizar tiempo, créditos y gasto adicional. Aplicar al planificar, ejecutar, revisar o retomar tareas.
version: 0.1.5
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

## Separación de conversaciones por entorno (v0.1.1)
- Crear, dentro de cada proyecto, tres hilos con nombres consistentes: `01 · CHAT — Dirección`, `02 · CODEX — Desarrollo`, `03 · WORK — Operaciones`. Son hilos de conversación, no tres procesos simultáneos.
- CHAT: única coordinación, decisiones, backlog, prioridades, análisis, documentación y asignación de tareas. Consultar siempre el estado maestro.
- CODEX: solo programación, refactorización, pruebas y depuración justificadas, con tarea y criterios de aceptación entregados desde CHAT.
- WORK: solo tareas gráficas o de navegador sin alternativa suficiente en Chat o conectores; nunca por rutina.
- Al cambiar de hilo se entrega una ficha con: ID de tarea, objetivo, estado previo, repositorio/rutas, restricciones, trabajos ya hechos, acciones permitidas, criterios de aceptación y formato de resultados.
- Al regresar, registrar en GitHub: ID, entorno, evidencia, archivos/commits, resultado, errores, decisiones y tarea siguiente. No cerrar sin verificación.
- Usar IDs estables (ej. BC-001) en los tres hilos. El archivo maestro en GitHub prevalece sobre recuerdos parciales; no afirmar que los hilos se sincronizan automáticamente.
- Word, si se trata de documentos .docx, será normalmente un entregable; no confundirlo con Work.
- Prohibido duplicar trabajo entre hilos o iniciar dos implementaciones de la misma tarea.

## Historial de versiones (continuación)
- **0.1.1 — 2026-10-18:** convenciones de hilos CHAT/CODEX/WORK y protocolo de traspaso y retorno con registro GitHub.

## Puerta obligatoria de fuentes antes de programar (v0.1.2)
- Antes de implementar recolectores de un proyecto de búsqueda, elaborar inventario exhaustivo razonable de fuentes necesarias y priorizarlas por objetivo.
- Recuperar pruebas anteriores y NO repetirlas sin justificación; cada fuente debe incluir URL, cobertura, clase de acceso (público/privado), método real, autenticación, estructura/API si consta, limitaciones, fecha y evidencia.
- Clasificar cada fuente como **verificada**, **parcial**, **bloqueada** o **pendiente**, distinguiendo ver una página en Chat de obtener los datos automáticamente en GitHub Actions.
- Primero comprobar vías gratuitas/legítimas y diagnosticar bloqueos; Work solo para interacción imprescindible.
- No comenzar implementación general sin inventario y decisión explícita sobre fuentes viables, limitadas y aplazadas. No exigir resolver absolutamente todas: justificar alcance y dependencias.
- Agrupar posteriormente la implementación y pruebas de las fuentes viables en Codex; no escribir conectores a ciegas.
- Documentar decisiones, evidencias y cuestiones abiertas en registro maestro del proyecto.
- **0.1.2 — 2026-10-18:** incorporar auditoría de fuentes como fase obligatoria previa a desarrollo.

## Continuidad autónoma hasta punto de intervención (v0.1.3)
**Regla vinculante:** una subtarea completada, un informe intermedio o un commit documental NO justifican finalizar el turno si el objetivo autorizado tiene tareas pendientes ejecutables sin el usuario.
1. Convertir el objetivo en una cola explícita de tareas ordenadas por dependencias; distinguir meta completa de hitos intermedios.
2. Tras cada hito, registrar avance y continuar automáticamente con el siguiente, sin preguntas ceremoniales ni «¿sigo?».
3. Informar mediante mensajes de progreso cuando el trabajo dure, pero no usar el progreso como excusa para detenerse.
4. Ante fallo: diagnosticar y usar alternativas gratuitas apropiadas; si una fuente está bloqueada, registrarlo y seguir otras independientes.
5. Parar solo por: objetivo alcanzado; autorización/credencial/decisión realmente imprescindible; riesgo de pago o seguridad; límite técnico real de herramienta, duración o alcance. Explicar exactamente qué impidió terminar y qué queda.
6. No prometer continuación después de terminar la respuesta; sin tarea programada el asistente no sigue trabajando en segundo plano.
7. Evitar frases de cierre del tipo «la próxima vez continuaremos» mientras existan tareas que puedan completarse ahora.
8. El presupuesto adicional por defecto sigue en cero; no activar Work/Codex ni automatizaciones por esta regla.
- **0.1.3 — 2026-10-18:** corregir paradas prematuras entre lotes de fuentes; continuar hasta punto de intervención real.

## Escalera de coste de conectores (v0.1.4)
**Obligatoria antes de pedir código:** seleccionar y justificar el mecanismo menos costoso que devuelva datos correctos y estables.
1. **API oficial pública, documentada y gratuita** o feed oficial (JSON, XML, RSS), si realmente ofrece los campos requeridos. Revisar autenticación, cuotas, cambios de esquema, términos y cualquier coste de uso.
2. **HTTP directo** de HTML, JSON, XML, ficheros o endpoints públicos legítimos: buscar listados, enlaces de fichas, paginación, fechas y campos estructurados. JSON público puede ser tan eficiente como una API. No asumir que un endpoint no documentado es estable ni que su acceso permite saltar controles.
3. **Navegador automatizado local/runner** solo si JavaScript o interacción imprescindible impiden la lectura HTTP; usar pruebas acotadas, no romper controles.
4. **Agente visual con IA / Work** únicamente para excepciones concretas; evitar su uso recurrente para scraping masivo.

- Registrar por fuente: método preferido, ruta pública, **evidencia** (HTML legible en Web vs verificado con urllib desde runner), datos realmente obtenidos, alternativas más económicas descartadas, paginación, periodicidad, autenticación, riesgos y coste adicional 0 €.
- La clasificación «parece HTML/HTTP» es hipótesis hasta que un runner reproduce resultados sin navegador; no atribuir API por encontrar un JSON en una página.
- Optimizar el volumen: comparar IDs/fechas/hashes, no redescargar sin necesidad, reintentos limitados, rate limiting razonable, tiempos/tamaños acotados y sin IA para cada oferta. IA solo para ambigüedad puntual.
- Cero gasto adicional por defecto y ninguna API tarifada, navegador de pago o evasión de barreras sin aprobación.
- **0.1.4 — 2026-10-18:** incorporar elección económica de protocolos y evidencia previa a Codex.

## Reutilización y descubrimiento de capacidades antes de desarrollar (v0.1.5)
Antes de programar funcionalidades no triviales:
1. Inspeccionar repositorio propio y dependencias ya existentes; preferir reutilización y pruebas ya verificadas.
2. Cuando aporte valor, investigar repositorios/librerías **públicos** de GitHub, contrastar licencia, mantenimiento, compatibilidad, seguridad, peso, dependencias y costes. No copiar código sin revisar permisos/licencias.
3. Revisar skills disponibles y documentación aplicable; **no asumir** que una skill Markdown almacenada en GitHub está instalada o accesible automáticamente en Codex.
4. Revisar conectores/plugins efectivamente disponibles en el entorno concreto, sus permisos y límites; no asumir que los conectores de ChatGPT se comparten con Codex.
5. Comparar explícitamente usar biblioteca, protocolo directo HTTP/API y código estándar propio; preferir el menor coste total y riesgo, no el mínimo código a cualquier precio.
6. Instalar, conectar o autorizar nuevas herramientas solo cuando sea necesario y con consentimiento si corresponde. Prohibidas dependencias o APIs de pago sin autorización expresa.
7. Documentar qué se buscó, qué se reutilizó, qué se descartó y por qué; realizar una investigación breve y enfocada, evitando búsquedas interminables que consuman cuota.
- **0.1.5 — 2026-10-18:** obligar a evaluar GitHub, skills y conectores antes de reinventar implementaciones.

## Desarrollo local primero y validación remota selectiva (v0.1.6)
**Regla general para proyectos con código y automatizaciones, cuando el acceso local exista y esté autorizado.**
1. Planificar e investigar con ChatGPT normal antes de utilizar Codex. Agrupar tareas relacionadas y reaprovechar diagnósticos, fixtures, código y evidencias existentes. El trabajo local **no elimina por sí mismo** el consumo de cuota de Codex: el ahorro de Codex proviene sobre todo de reducir iteraciones redundantes y delegaciones innecesarias.
2. Inspeccionar `git status`, rama y commit antes de editar; sincronizar de manera segura (solo fast-forward si procede) y no sobrescribir cambios locales. Preferir **una única copia local** ya enlazada a su repositorio.
3. Implementar en esa copia local y ejecutar allí primero linters, tests unitarios, integración con mocks/fixtures y simulaciones de varias ejecuciones sin descargar otra vez datos de los portales. Agrupar pruebas y corregir fallos antes del primer run remoto.
4. Usar GitHub Actions y otros runners remotos solo cuando aporten evidencia que no pueda obtenerse localmente: entorno Linux real, red desde runner, persistencia de artefactos entre runs, permisos, integración o reproducibilidad de despliegue. Una ejecución de validación suele bastar; una segunda cuando la persistencia, idempotencia o el criterio de aceptación lo exija. No imponer una cantidad fija de runs si aparecen fallos reales.
5. Comparar coste **total**: cuota de Codex/IA, minutos Actions, bytes de red, almacenamiento, tiempo humano y fiabilidad. Desarrollar localmente ahorra minutos y artefactos remotos, pero no necesariamente créditos de Codex ni tokens de ChatGPT.
6. Registrar número de pruebas locales y ejecuciones remotas, qué verificó cada una y por qué fue necesaria; evitar reruns idénticos sin hipótesis nueva. No reducir cobertura ni declarar validación remota si solo se hicieron pruebas locales.
7. La **operación diaria definitiva puede y debe permanecer en el runner gratuito** si es el diseño acordado; desarrollar localmente no implica depender de un PC encendido en producción. Sin llamadas a modelos IA en ejecuciones automáticas, salvo autorización explícita.
8. Respetar autorizaciones vigentes: **no ejecutar acciones remotas/manuales, activar cron, usar credenciales ni introducir gastos** cuando la tarea exija permiso específico. Mantener por defecto presupuesto adicional 0 €; verificar tarifas y límites de facturación cuando sean relevantes.
9. Si no hay acceso real al equipo local o este no está disponible, no simularlo ni bloquearse artificialmente: utilizar una alternativa gratuita y verificable, explicando la diferencia y los costes/limitaciones.
- **0.1.6 — 2026-10-19:** normalizar «desarrollo y pruebas locales primero, validación GitHub selectiva», sin confundir ahorro de Actions con ahorro automático de créditos Codex.
