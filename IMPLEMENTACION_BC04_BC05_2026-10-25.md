# Buscar Curro — implementación BC-04/BC-05 (25-10-2026)

**Alcance:** desarrollo y pruebas locales. Fuente canónica: `vtsalamanca/Buscar-Curro`. Base `399e3f7`. Rama `mejora-bc04-bc05`, worktree limpio inicial creado en Debian sin alterar la copia migrada ni `main`.

## Cambios implementados
- `state_safety.py`: estados estructuralmente validados, escritura atómica con fsync, ZIP local de recuperación con hash SHA-256, rechazo de symlinks/archivos dañados y límites de tamaño. `state_snapshot_cli.py`: crear, inspeccionar o recuperar un snapshot **sin red**; no se instalan servicios ni se guardan secretos.
- `restore_previous_state.py`: validación del tamaño descomprimido y restauración atómica. Si el artefacto anterior ha caducado sigue fallando de forma cerrada; no reinicia falsamente el histórico.
- `public_connectors.py`: límites reales por ejecución de 70 peticiones HTTP, 50 MiB de tráfico y 600 segundos, además de límite de 9 MiB de archivos de salida. Su agotamiento produce error, no «sin novedades».
- Workflows BC-02, BC-03, ETT-01 y BT-01B: mismo grupo de concurrencia, no cancelan ejecución en curso; se elimina duplicación de state.json en diagnósticos; éstos se suben solo si hubo éxito. **Siguen manuales**, sin cron.
- Errores de detalle: estados `consulta_parcial` y `source_failures`, conservando lo recuperado sin declarar ausencia de cambios.
- `bc02_quality.py`: diferenciar requisito obligatorio, valorable o negado para títulos profesionales regulados. Se conservan dudas cuando la habilitación no consta.
- `employment_core.py`: evitar falsos positivos de «operario con certificado de discapacidad»; mantener puestos de atención a la discapacidad y educación.
- `offer_review.py`: preselección JSON explicable, prioridad, motivos y URLs. Solo agrupa anuncios de proveedores distintos cuando están acreditados empleador, título, municipio, provincia y fecha; sin empresa identificada no fusiona.
- `run_public_sources.py`: evaluación geográfica y profesional común; 259 municipios y kilómetros **en línea recta**, no por carretera. Salida `review-provisional.json` solo diagnóstica, NO constituye el informe final del usuario.

## Evidencia y protección histórica
Se restauró como archivo adjunto de la conversación el artefacto BC-03 del run `39255609713` (19/10/2026), con caducidad 18/11/2026. Estado comprobado: **317 candidatas = 267 comprobadas, 30 filtradas, 19 errores y 1 no listada**, 0 pendientes activas y 5 documentos normalizados. El nuevo ZIP de respaldo contiene manifest de integridad SHA-256. No se han subido estos datos al código GitHub.

Batería nueva antes de publicación: **77/77 pruebas locales OK**, incluidas regresiones de candidaturas, permisos de snapshot, corrupción, límites de red, errores parciales, falso positivo Randstad y requisitos educativos. Compilación y `git diff --check` superados. Verificar resultado remoto por separado.

## Límite pendiente antes de autonomía diaria
El histórico por artefactos de GitHub Actions **sigue expirando a los 30 días**. La copia manual no lo convierte en almacenamiento remoto indefinido. Falta método duradero aprobado, verificación de facturación/cuotas en cuenta y prueba integral en Actions antes de activar cron; por tanto NO se ha activado. También quedan pendientes BC-06 (más fuentes y cobertura), BC-07 (formato elegido por el usuario), BC-08 (automatización condicionada) y BC-09 (integraciones opcionales). Sin pagos, APIs de IA, credenciales, CAPTCHAs sorteados ni candidaturas automáticas.

## Manual local
`python3 state_snapshot_cli.py inspect --archive copia.snapshot.zip`
`python3 state_snapshot_cli.py restore --archive copia.snapshot.zip --state data/bc03-state.json`

Las restauraciones de datos reales requieren identificar el archivo de origen y no sobrescribir un estado actualizado. Los snapshots tienen comprobación de integridad, **no firma criptográfica de autor**.
