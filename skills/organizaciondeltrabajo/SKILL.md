---
name: organizaciondeltrabajo
description: Metodología general predeterminada de planificación y ejecución eficiente. Aplicar al iniciar, retomar, organizar o cambiar de fase de un trabajo no trivial: recuperar contexto y skills, elegir entorno de menor coste, agrupar pruebas, continuar hasta bloqueo real y verificar resultados. Presupuesto adicional cero.
version: 0.2.1
---
# &organizaciondeltrabajo — metodología general

## Alcance y activación
Aplicar proactivamente al iniciar, retomar o cambiar de fase de tareas no triviales, si el entorno permite descubrir esta skill. Esta declaración NO garantiza invocación automática desde todos los chats o proyectos: se complementa con instrucciones personalizadas y de proyecto. Para cuestiones triviales, omitir ceremonia.

**Fuente única de verdad:** `vtsalamanca/Buscar-Curro/skills/organizaciondeltrabajo/SKILL.md`. Esta versión consolida la línea 0.1.0–0.1.6 del repositorio y las mejoras 0.2.0 del plugin. ChatGPT y Codex pueden usar copias empaquetadas o cacheadas, pero deben reproducir este archivo canónico; un Markdown en GitHub no se instala ni se actualiza automáticamente.

## Misión y garantías
Conseguir resultados fiables y verificables con el menor gasto razonable de tiempo del usuario, operaciones manuales, créditos, cuotas y dinero. Presupuesto adicional por defecto **0 €**. Nunca utilizar servicio/API/plugin/ejecutor de pago por uso, aun con saldo promocional, sin comprobar tarifa, saldo y coste estimado y obtener autorización expresa por operación. Si coste desconocido, bloquear. No comprometer calidad, seguridad, legalidad ni verificabilidad por ahorrar.

## Puerta de eficiencia antes de actuar
1. Recuperar objetivo, limitaciones, autorizaciones, estado maestro y decisiones previas; examinar primero resultados, pruebas, archivos y repositorios. Distinguir VERIFICADO, COMUNICADO, HIPÓTESIS, PENDIENTE, BLOQUEADO y DESCARTADO.
2. Descubrir skills y conectores **realmente disponibles** para este entorno, revisar permisos y coste antes de inventar soluciones. No suponer que Chat, Codex y Work comparten capacidades. Reutilizar código/librerías compatibles previa auditoría de licencia, seguridad y mantenimiento.
3. Elegir la ruta de menor **coste total efectivo**, incluyendo minutos, créditos, riesgo y esfuerzo del usuario: (a) razonamiento/inspección en Chat; (b) análisis estático y prueba local o simulada; (c) API/feed oficial público y gratuito; (d) HTTP HTML/JSON autorizado; (e) navegador local/runner cuando sea imprescindible; (f) Codex para programación compleja; (g) Work para interacción gráfica excepcional. Orden adaptable a las necesidades técnicas, no rígido.
4. En proyectos de software, estudiar si una inspección o prueba local resuelve la duda antes de crear workflow. **No usar GitHub Actions como laboratorio iterativo** cuando pruebas locales o análisis en lote den la misma evidencia.
5. Definir entregable, criterios de aceptación, dependencias, seguridad, plan de pruebas y reversión; agrupar las comprobaciones que responden a una misma hipótesis. No generar un commit, workflow y ejecución por una búsqueda simple de texto.
6. Preguntar al usuario solo por autorizaciones o decisiones realmente imprescindibles; evitar ciclos ceremoniales «ya / vale» cuando haya trabajo independiente realizable. Continuar hasta objetivo logrado o bloqueo real.

## Distribución de trabajo
- **Chat:** coordinación, contexto, investigación, análisis, decisiones, documentación y consultas mediante conectores disponibles; opción inicial.
- **Análisis local:** inspección, pruebas estáticas, fixtures sintéticos, extracción de datos y depuración sin servicios externos cuando estén disponibles. No prometer acceso a PC si no está autorizado.
- **Codex:** implementación, refactorización y pruebas que justifiquen su cuota; agrupar un encargo coherente.
- **Work:** flujos UI/navegador y operaciones complejas que no tengan alternativa suficiente; no usar por rutina ni cambiar de modo sin intervención del usuario.
- **GitHub:** código, historial, fuente de verdad, integraciones y automatización definitiva; CI puntual tras validación local. GitHub público no significa que los datos escolares, credenciales o logs deban ser públicos. Secreto en repositorio público requiere revisar el código ejecutado y limitar permisos.

## Desarrollo local primero y validación remota selectiva
Cuando exista acceso local autorizado, inspeccionar estado de Git, rama y commit antes de editar; no sobrescribir cambios locales y preferir una única copia enlazada al repositorio. Implementar y probar primero localmente con linters, tests, fixtures, mocks y simulaciones reutilizables. Reservar GitHub Actions u otros runners para evidencia que no pueda obtenerse localmente —entorno, red, permisos, persistencia o integración— y evitar reejecuciones idénticas sin una hipótesis nueva. Registrar qué verificó cada prueba local y remota. La operación diaria definitiva puede seguir en un runner incluido si ése es el diseño acordado; no introducir llamadas a modelos, credenciales, cron ni gasto sin autorización. El trabajo local reduce iteraciones y minutos remotos, pero no implica por sí mismo menor cuota de Codex.

## Flujo de coordinación y aprendizaje
**A. Recuperar:** consultar `ESTADO_PROYECTO.md` o registro equivalente, decisiones y pruebas; resolver contradicciones.
**B. Planificar:** objetivo medible, restricciones, fuentes necesarias, criterios de aceptación y bloques según dependencias. En recolectores auditar fuentes antes de programar: URL, método, cobertura, autenticación, evidencia, estado y limitaciones; no exigir resolver todas si la exclusión está justificada.
**C. Ejecutar:** cambios mínimos y reversibles; agrupar diagnóstico + pruebas; no duplicar entre conversaciones. Si aparece fallo, aislar capa (origen/red/autenticación/extracción/deduplicación/almacenamiento/entrega), buscar causa y probar hipótesis falsable; máximo un reintento ante fallo transitorio salvo nueva evidencia.
**D. Verificar:** distinguir diseñado, guardado, ejecutado, probado localmente y validado extremo a extremo. No afirmar éxito por existir archivo, commit, HTTP 200 o workflow verde sin comprobar el objetivo real. Fecha, versión y evidencia.
**E. Aprender:** registrar causa de repetición o desperdicio, mejora medible y comparación esfuerzo previsto/real; proponer incremento de versión sin alterar silenciosamente criterios esenciales.

## Escalera para recolectores
1. API/feed oficial público gratuito documentado; 2. HTTP autorizado con HTML/JSON/XML; 3. navegador automatizado solo cuando la interacción JavaScript sea imprescindible; 4. agente visual/Work solo excepciones. Registrar evidencia real, reintentos limitados, paginación, cuotas y límites de tiempo/tamaño. No confundir JSON público con API documentada; no eludir controles de acceso.

## Tres conversaciones por proyecto cuando ayuden
`01 · CHAT — Dirección`; `02 · CODEX — Desarrollo`; `03 · WORK — Operaciones`. Al transferir tareas llevar ID, objetivo, estado, rutas, límites, autorizaciones y pruebas; al volver actualizar estado maestro. No es obligación crear hilos nuevos si solo añade fricción.

## Registro mínimo
`ID | Proyecto | Objetivo | Entorno | Estado | Evidencia | Dependencias | Coste autorizado | Siguiente paso`.
Continuar automáticamente al siguiente bloque permitido después de cada hito. Parar únicamente por objetivo terminado, decisión/credencial/autorización necesaria, riesgo, o límite técnico real. No prometer actividad en segundo plano sin tarea programada.

## Ingeniería técnica especializada
Cuando haya programación, fallos, pruebas o despliegues, consultar **`ingenieria-fiable`** y sus referencias para ciclo rojo-verde-refactor, diagnósticos por capas, pruebas y compuerta de verificación. Esta skill coordina la elección de herramientas y recursos; `ingenieria-fiable` profundiza en comprobación técnica, evitando duplicación.

## Caso aprendido: Educamos, octubre 2026
Se realizaron demasiados ciclos manuales de editar Python en GitHub → commit → GitHub Actions → log para localizar partes de JavaScript. Antes de repetir ese patrón: recuperar el APK/código y JS disponible, analizar estáticamente/localmente, agrupar hipótesis y pruebas, reservar GitHub Actions para verificar integración y funcionamiento diario. Considerar tiempo y clics del usuario como recurso; evitar optimizar minutos gratis a costa de esfuerzo humano.

## Historial
- 0.1.0–0.1.5 (18 oct 2026): protocolo original en `vtsalamanca/Buscar-Curro`; continuidad, auditoría de fuentes, elección HTTP/API y descubrimiento de capacidades.
- 0.1.6 (19 oct 2026): desarrollo y pruebas locales primero; validación remota selectiva y medición del coste total.
- 0.2.0 (19 oct 2026): integración en Gestor de Skills; activación proactiva donde sea posible, puerta obligatoria de eficiencia, preferencia local, caso Educamos y enlace a ingenieria-fiable.
- 0.2.1 (19 oct 2026): unificación de 0.1.6 y 0.2.0; GitHub pasa a ser la fuente única de verdad y las copias empaquetadas deben reproducirla.
