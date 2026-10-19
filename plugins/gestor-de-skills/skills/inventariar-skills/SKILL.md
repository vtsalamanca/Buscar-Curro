---
name: inventariar-skills
description: Inventaría skills y plugins existentes, detecta duplicados, registra versiones y planifica actualizaciones seguras sin reinstalar ni actualizar automáticamente.
---
# Inventariar skills

## Procedimiento
1. Lee primero el catálogo de skills habilitadas y los plugins disponibles con las herramientas de la sesión. No atribuyas acceso a dispositivos remotos no conectados.
2. Construye una ficha por skill: nombre, finalidad, plataforma, origen, versión conocida, permisos, coste marginal, último análisis, riesgos y evidencia. Marca como desconocido lo no verificable.
3. Agrupa funciones similares, detecta duplicados por objetivo/entorno, y recomienda reutilizar, fusionar o separar. No desinstales por iniciativa propia.
4. Para propuestas de actualización, compara notas, archivos modificados, dependencias y coste con la versión anterior; solicita auditoría estática mediante `auditar-skills`.
5. Da prioridades por impacto: seguridad, incompatibilidad, obsolescencia, mantenimiento o valor real. No actualizar para subir números sin beneficio.
6. Presenta inventario exportable como tabla o Markdown/CSV si se solicita. Si se requiere persistirlo fuera de la conversación, pide destino o utiliza el ya expresamente indicado; no afirmes que hay una base de datos continua sin ella.
7. Cualquier publicación, instalación, desinstalación o cambio persistente requiere la autorización pertinente. Para operación facturable, presupuesto cero hasta tarifa/saldo/coste y autorización explícita.

## Salida
Resumen de cobertura, duplicados, elementos a revisar y recomendación priorizada. Indica fechas de comprobación y **desconocido** cuando no pueda comprobarse mantenimiento/versión.
