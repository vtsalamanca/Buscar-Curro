# Evaluación avanzada de skills

## Puntuación reproducible (0 a 100; no es certificación de seguridad)
- Adecuación concreta a la tarea: 0–25.
- Legitimidad y evidencia de fuente: 0–20.
- Compatibilidad demostrada con el entorno: 0–20.
- Permisos mínimos y resultado de auditoría estática: 0–20.
- Mantenimiento, documentación, pruebas y licencias: 0–10.
- Operación viable con presupuesto marginal cero verificado: 0–5.
No suplir evidencias desconocidas con puntuación máxima; marcar «desconocido». Bloqueo independientemente de la nota si hay exfiltración, prompt injection operativa, costes no autorizados o ausencia de archivos esenciales.

## Ficha de candidata
Nombre | URL original | Autor/commit o versión | Licencia | Qué resuelve | Alternativas ya instaladas | Cliente de destino | Dependencias | Permisos | Coste comprobado/no comprobado | Evidencia revisada | Riesgos | Puntuación | Estado (recomendada/condicionada/descartada/pendiente).

## Pruebas sin ejecutar código remoto
A. Coincidencia real por tarea y sinónimos (evitar coincidencia superficial).
B. Duplicado local: recomendar reutilización en vez de instalación.
C. Repositorio sin SKILL.md: marcar como no verificable.
D. Skill con scripts ocultos o comandos `curl | sh`: detener instalación.
E. Dependencia con precio desconocido: detener ejecución y mantener presupuesto 0 €.
F. Incompatibilidad ChatGPT vs CLI: distinguir instrucciones reutilizables de instalación real.
G. Fuente caída o autenticación exigida: reportar incidencia y alternativa, sin bucles.
H. Usuario solicita modificación: verificar autorización, identificar versión, aplicar cambio mínimo, leer de nuevo y ofrecer rollback.

## Estrategia de búsqueda
Buscar primero por tarea específica; ampliar a sinónimos inglés/español y al repositorio canónico. Skills.sh es índice, no prueba de legitimidad. Popularidad y estrellas son señales auxiliares. Priorizar lectura estática por encima de instalación de CLI. Conservar hasta tres recomendaciones no redundantes.
