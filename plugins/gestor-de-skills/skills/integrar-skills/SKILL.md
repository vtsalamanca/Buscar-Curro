---
name: integrar-skills
description: Planifica cómo incorporar una skill en ChatGPT, Codex, Claude, un agente local o GitHub Actions; comprueba compatibilidad, permisos, validación y coste sin instalar sin aprobación.
---
# Integrar skills por entorno

## Ruta de integración
1. Identifica el destino real y comprueba si ya existe la capacidad. Distingue siempre ChatGPT (plugin privado/skills disponibles), Codex, agentes CLI locales y repositorios/workflows de GitHub.
2. Revisa previamente con `auditar-skills`; si el riesgo es alto o faltan archivos críticos, detener la instalación.
3. Identifica la variante más simple: instrucciones en una skill sin scripts; skill + referencias; plugin privado con varias skills; agente local; automatización GitHub Actions separada del archivo SKILL.md.
4. Prepara un plan en pasos con dependencias, permisos, ruta de configuración, pruebas sin coste y rollback. No prometas que Skills.sh se instala automáticamente en ChatGPT.
5. Antes de cambiar archivos, publicar, instalar, habilitar tareas, crear tokens, conectar cuentas o ejecutar instaladores, solicita aprobación explícita. Si la autorización ya está clara en el contexto, reutilízala solo dentro del alcance concedido.
6. Tras un cambio autorizado, verifica presencia de archivos, identificación de versión, capacidad de lectura, prueba mínima inofensiva y comportamiento de retorno a versión anterior.

## Perfiles
**ChatGPT:** si se tiene permiso para editar el plugin existente, conserva ID, nombre, estructura y controles, modifica solo lo necesario, actualiza versión y verifica con lectura de archivos. No afirmes que ejecutar `npx skills add` añade una habilidad al plugin de ChatGPT.

**Codex/agentes locales:** verificar documentación del cliente, sistema operativo y ubicación correcta antes de ofrecer un comando. Inspeccionar primero y no ejecutar por defecto.

**GitHub Actions:** un `SKILL.md` por sí solo no ejecuta una tarea programada. La integración requiere workflow, código y mecanismo de entrega; credenciales siempre en secretos del repositorio. En público, runners estándar pueden estar incluidos; en privado hay cuotas y el uso adicional puede ser facturable. Runners grandes o APIs de terceros pueden generar cargos incluso en repositorio público. No iniciar trabajos si no está acreditado coste 0 para la operación.

## Entregables
Compatibilidad por entorno (confirmada / pendiente / incompatible), requisitos, arquitectura, pasos de instalación con aprobación pendiente, pruebas, coste marginal esperado y rollback. No repetir preguntas resueltas.
