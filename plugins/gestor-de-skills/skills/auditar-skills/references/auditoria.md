# Lista de comprobación de auditoría de skills (estática)

## Procedencia
- Autor, repositorio canónico, versión o commit SHA, licencia, fecha de último cambio, incidencias abiertas conocidas.
- Si se dispone solo de una página resumen, marcar evidencia incompleta hasta revisar los archivos reales.

## Archivos y comportamiento
- Frontmatter válido y propósito explícito.
- Examinar `SKILL.md`, `scripts/`, workflows `.github/workflows/`, `package.json`, lockfiles, `requirements.txt`, `pyproject.toml`, comandos en documentación.
- Evitar descargar y ejecutar paquetes como parte de la auditoría.
- Identificar permisos y acciones concretas: lectura/escritura, red, GitHub, ejecución de código, claves, acceso al sistema, cambios persistentes.

## Señales de alerta
- Lectura de secretos, `.env`, carpetas personales completas, tokens, credenciales, certificados privados.
- Publicación o transmisión a URLs no documentadas; ejecución remota sin revisión, instaladores opacos.
- Prompt injection (`ignora instrucciones previas`, redirige sesión, revela secretos, utiliza permisos adicionales).
- Dependencias sin fijar, bins precompilados opacos, hooks de instalación, comandos destructivos (`rm -rf`, borrado de credenciales), permisos innecesarios.
- Servicios facturables, pruebas que generan costos, endpoints no documentados.

## Escala
- Crítico: exfiltración probable, ejecución arbitraria no controlada, secretos o gasto no autorizado.
- Alto: dependencia remota no auditada, privilegios excesivos, costes sin límites.
- Medio: instalación compleja, mantenimiento pobre, dependencias no fijadas.
- Bajo: documentación mejorable, detalles opcionales no verificados.

No atribuir al autor intenciones maliciosas sin pruebas; diferenciar riesgo de confirmación. Sin acceso al código completo, **no certificar seguridad**.
