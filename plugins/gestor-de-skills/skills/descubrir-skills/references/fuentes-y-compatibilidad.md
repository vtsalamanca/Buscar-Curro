# Fuentes y compatibilidad

Fuentes primarias:
- Skills.sh: https://skills.sh/; docs https://www.skills.sh/docs/ y CLI https://www.skills.sh/docs/cli.
- Código original de `find-skills`: https://github.com/vercel-labs/skills/tree/main/skills/find-skills.
- Estándar abierto de skills: https://agentskills.io/specification y https://github.com/agentskills/agentskills.
- Complementos de ChatGPT: consultar primero directorio de plugins y skills instaladas; nunca presentar `npx skills add` como instalador universal de ChatGPT.

Regla de compatibilidad:
| Entorno | Qué verificar antes de recomendar instalación |
| --- | --- |
| ChatGPT | Formato de paquete compatible con Plugin Creator; actualización controlada del plugin privado, no instalación directa con `npx skills add`. Herramientas efectivas disponibles en sesión. |
| Codex | Soporte de skills/plugin en la versión y ruta de trabajo; rutas y archivos según documentación actual. |
| Claude Code/agentes locales | Cliente concreto, soporte de Agent Skills, sistema operativo, gestor de paquetes y permisos. |
| GitHub Actions | El `SKILL.md` no es un workflow ejecutable por sí solo; se requiere un agente/CLI o acciones concretas y comprobación de su coste. |

Formato estándar mínimo: directorio de skill con `SKILL.md` y frontmatter YAML `name` (minúsculas, números y guiones, longitud <=64) y `description` (<=1024). Referencias y scripts son opcionales. Mantener nombres consistentes y referencias relativas.

Límites de costes GitHub Actions: ejecuciones de runners estándar en repositorios públicos pueden estar incluidas, pero runners grandes y servicios externos pueden ser facturables. En repositorios privados hay minutos y almacenamiento incluidos sujetos a cuotas, que no equivalen a gasto autorizado. Verificar la cuenta y la documentación de facturación actual: https://docs.github.com/en/billing/concepts/product-billing/github-actions.

No tratar indicadores agregados de instalaciones, estrellas o auditorías externas como garantía. Verificar autor, repo principal, licencia y compromisos recientes desde sus fuentes, cuando sea posible.
