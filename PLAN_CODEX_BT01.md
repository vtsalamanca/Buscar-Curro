# Buscar-Curro — Encargo agrupado para Codex BT-01

**Estado:** preparado, NO autorizado para ejecución. Fecha: 2026-10-18.
**Presupuesto adicional:** 0 €. No contratar API, servicios de pago o infraestructura. Revisar límites antes de ejecutar trabajos con cuota.
**Repositorio:** `vtsalamanca/Buscar-Curro`; carpeta Windows `C:\Users\Usuario\Desktop\Buscar curro`.
**Documento de referencia:** `ESTADO_PROYECTO.md`, `SOURCES_STATUS.md`, `AUTH_STATUS.md` y `skills/organizaciondeltrabajo/SKILL.md`.

## Objetivo
Probar primero qué fuentes públicas son realmente consultables desde el entorno de GitHub Actions. Implementar solo los conectores viables cuando el usuario autorice la segunda parte. No ejecutar el programa completo durante la fase documental.

## BT-01A: prueba de acceso automatizable (primera intervención técnica)
1. Inspeccionar sin modificar el código ATE existente, cinco workflows y sus pruebas; reutilizar patrones seguros.
2. Construir pruebas de diagnóstico públicas, idempotentes, de tiempo y tamaño limitados para: DOCM/BOE/BOP Toledo/JCCM, Empleo CLM/Empléate/Toledo/Nambroca/Aranjuez, Trama/ILUNION/Cruz Roja y ACCEM si existe URL oficial directa validada.
3. Para cada fuente registrar: URL, fecha, respuesta HTTP, redirecciones, si el contenido incluye resultados y enlaces reales, paginación/estructura, si precisa JS/login, posibles límites y errores. Guardar sólo metadatos públicos sanitizados, nunca secretos o datos de aspirantes.
4. No asumir que una página abierta equivale a búsqueda funcional, ni que respuesta 200 implica ofertas extraíbles.
5. Usar pruebas unitarias locales con ejemplos HTML públicos y test de errores; pruebas remotas limitadas, sin bucles agresivos ni elusión de controles.
6. Resultados en un informe por fuente: `verificada_desde_runner`, `parcial`, `bloqueada`, `no_probada`; evidencia reproducible con commit y run.
7. Si hay fuentes bloqueadas, pasar a las demás; no repetir intentos sin diagnóstico. No tocar ATE privado ni InfoJobs autenticado.
8. No activar cron, no solicitar credenciales, no enviar solicitudes de empleo, no modificar perfil, correo ni el código de producción existente.
9. La puesta en marcha de pruebas que consuman cuota o requieren autorizar GitHub Actions se debe aprobar explícitamente y verificar coste adicional cero.

### Criterio de salida BT-01A
Una matriz de evidencia reproducible que permita decidir cuáles de las fuentes son viables para implementar, con limitaciones claras y sin alterar funcionalidades existentes.

## BT-01B: implementación agrupada (solo después de BT-01A aprobado)
- Construir conectores solo para rutas verificadas.
- Datos comunes: fuente, ID documento/puesto, proceso, título, categoría, municipio/provincia, fecha publicación, plazo, URL oficial, requisitos comprobados, estado, hash y errores.
- Relacionar documentos (p. ej. convocatoria BOP + BOE + corrección) sin descartar actos distintos.
- Distinguir «sin novedades» de «no se pudo consultar».
- Perfil activo: ATE Toledo, psicología no sanitaria, menores, intervención social, educación y discapacidad. Logística y almacén suspendidos.
- Evitar recomendar plazas que exigen titulaciones o habilitaciones no acreditadas.
- Persistencia de resultados y deduplicación verificables; test con casos históricos DOCM y ayuntamientos.
- Comparar frente a tests ATE existentes; documentar regresiones y reversión.
- Sin activación diaria ni notificaciones hasta aprobación posterior.

## Traspaso de vuelta a Chat
Devolver: cambios concretos, tests ejecutados, commits, URLs de evidencias, estado por fuente, bloqueos y próximos pasos. Actualizar `ESTADO_PROYECTO.md` manteniendo estados de evidencia precisos.

**No comenzar BT-01A ni BT-01B por el mero hecho de encontrar este archivo. Es una especificación, no una orden de ejecución.**

## Comprobación económica y puerta de ejecución (18/10/2026)
- Repositorio identificado como **público** por búsqueda de GitHub; rama principal `main`.
- Documentación oficial GitHub Actions: los **runners estándar de GitHub en repositorios públicos** son gratuitos; los *larger runners* siempre pueden generar cargos y el almacenamiento de artefactos/caché debe respetar límites del plan: https://docs.github.com/en/billing/concepts/product-billing/github-actions .
- Diseñar BT-01A con `ubuntu-latest` estándar, temporizador estricto, sin artefactos grandes ni servicios externos de pago. Antes de cada nueva dependencia comprobar que no tiene tarifa por uso.
- **No confundir presupuesto adicional 0 € con cuota Codex gratuita/infinita:** no se ha verificado cuota de Codex ni se ha consumido para este análisis. El usuario puede abrir el hilo Codex existente y solicitar allí el bloque ya preparado.
- Requiere operación dentro de Codex para modificar/ensayar código; no afirmar que el acceso automático a nuevas fuentes está probado antes de ver el run real.
