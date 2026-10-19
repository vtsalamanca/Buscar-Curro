# Buscar-Curro — Política de eficiencia, recursos y presupuesto cero

**Fecha:** 19 de octubre de 2026. **Estado:** planificación; pendiente de implementación y validación. **Presupuesto adicional autorizado: 0 €**.

## Objetivo y arquitectura acordada
Aplicación autónoma gratuita, fiable, diaria sin PC encendido y sin usar tokens/créditos de ChatGPT en ejecuciones cotidianas. Repositorio público `vtsalamanca/Buscar-Curro`; GitHub Actions con runners Linux estándar; Python estándar/HTTP para extracción, filtros, deduplicación e histórico; ChatGPT para planificación; Codex para desarrollo/depuración/pruebas cuando aporte valor; Work excepcional. **No incorporar API de IA al flujo diario.**

## Límites propuestos para fase operativa (NO activos por este documento)
| Recurso | Límite |
|---|---|
| Ejecuciones automáticas | 1 por día |
| Duración máxima por ejecución | 15 minutos |
| Artefactos generados por ejecución | 10 MB en total |
| Retención de artefactos diarios de diagnóstico | 7 días |
| Ejecuciones simultáneas | 1 |
| Ejecutor | Linux estándar gratuito |
| Repositorio | Público |
| Presupuesto externo / APIs y servicios de pago | 0 €; requieren permiso expreso |

Los límites de minutos, tamaño de ZIP/artefactos, petición HTTP, bytes descargados, reintentos, concurrencia e integridad del estado deberán implementarse/probarse expresamente. Los límites de aplicación no sustituyen controles de facturación.

## Consumo orientativo, NO medición
30 runs/mes × 15 minutos = **450 minutos máximos teóricos**; 7 × 10 MB = **70 MB** de artefactos diarios simultáneos (sin otros workflows). La cifra de 500 MB como cuota incluida y la estimación de 14 % **requieren verificación en la cuenta y en el plan vigente**, y el almacenamiento es compartido con otros usos. Un artefacto BT-01B de referencia ~13,4 KB fue citado por el usuario, no comprobado aquí. No afirmar que no puedan existir cargos hasta inspeccionar presupuestos/controles reales. Las acciones estándar en repositorios públicos son gratuitas según documentación actual de GitHub; *larger runners* son facturables. Fuente: https://docs.github.com/en/billing/concepts/product-billing/github-actions y https://docs.github.com/en/billing/how-tos/set-up-budgets .

## Prevención de gasto
- Antes del cron, comprobar en GitHub > Settings > Billing & licensing > Budgets and alerts los controles aplicables y bloqueos de gasto; presupuesto 0 USD con parada donde sea factible. Si no es posible comprobar, no declarar blindaje de cargos.
- Sin runners premium, dependencias de pago ni servicios externos tarificados. Uso limitado de HTTP, bytes, tiempos, reintentos, y ejecución concurrente.
- Evitar ejecuciones repetitivas. Registrar interrupciones como fallos, no `cero ofertas`.
- Monitorizar cuotas/uso. No activar nada sin autorización.

## Ligereza y fiabilidad
- Mantener cola BC-02, deduplicación y hashes, CSV precargado de 259 municipios (80 km aproximados por línea recta desde Nambroca).
- Consultas y descargas incrementales, clasificación determinista sin IA, priorización por relevancia, continuidad de histórico.
- Métricas por fuente: HTTP, bytes, tiempo, candidatas, examinadas, pendientes, cobertura parcial y errores.
- Ningún ahorro justifica pérdida silenciosa de ofertas.
- Desarrollo eficiente: investigar/reutilizar, agrupar encargos Codex, usar Chat normal, evitar Work, herramientas y créditos adicionales. Estimación aportada de 80–200 créditos equivalentes Codex (central 140) es **hipótesis no contrastada** y no debe tratarse como presupuesto comprometido.
- Informes personales se definirán después, sin anticipar su diseño.

## Auditoría de compatibilidad del repositorio — 19/10/2026
Se inspeccionaron `.github/workflows/bc02.yml`, `ett01.yml` y `bt01b-public-sources.yml` y `PLAN_BC03_COBERTURA_PROGRESIVA.md`.
- **Compatible ya:** runners Linux estándar (ubuntu-24.04/ubuntu-latest), repositorio público, workflows solo `workflow_dispatch` (sin ejecución recurrente), `concurrency` sin cancelación, permisos mínimos `contents:read/actions:read`, sin API OpenAI.
- **Diferencias pendientes:** 12 minutos `timeout-minutes` actual frente a límite planificado de 15 (12 es más estricto y válido); no hay `schedule` diario; workflows BC-02, ETT-01 y BT-01B mantienen *estado* con artefactos 30 días y *diagnóstico* con 7 días; la norma de retención 7 días **solo debe aplicarse a diagnósticos**, salvo diseñar y verificar previamente histórico persistente que no caduque a 7 días. No recortar el estado a 7 días y perder deduplicación. El límite de 10 MB TOTAL por ejecución no está probado ni impuesto por workflows. `concurrency` se aplica por grupo distinto en cada workflow; no impide solapamientos *entre* BC-02, ETT-01 y BT-01B. La frecuencia de pruebas completas antes de cada ejecución operativa deberá analizarse para ahorrar tiempo sin reducir garantías.
- **Facturación:** no se ha accedido a la configuración privada del titular; seguridad de gasto 0 € no verificada. Documento normativo de GitHub: https://docs.github.com/en/billing/how-tos/set-up-budgets .
- **BC-03:** mantenerlo manual en esta fase, respetando presupuesto 0 y sus límites; activación diaria es fase aparte con autorización expresa.
- **Criterio de permisos de ejecución manual:** cada nueva ejecución de prueba requiere autorización; la recepción de esta política NO la otorga.

## Puertas antes del funcionamiento diario
1. Verificar facturación/bloqueos de gastos del titular y otros workflows.
2. Unificar o coordinar el límite de concurrencia de los workflows operativos.
3. Añadir límites efectivos de bytes, HTTP y tamaño de artefactos, medirlos y comprobar su agotamiento seguro.
4. Resolver persistencia del estado con 7 días de diagnóstico, sin falsos nuevos.
5. Comprobar suficiente cobertura diaria, incluida paginación BC-03.
6. Validar resultados y registrar evidencia técnica en repositorio.
7. **Solo entonces solicitar autorización independiente para activar 1 cron/día**.

**Principio permanente:** gastar recursos de desarrollo en construir la aplicación, no en consumir IA en cada ejecución. Este documento por sí solo no modifica código, workflows ni facturación.
