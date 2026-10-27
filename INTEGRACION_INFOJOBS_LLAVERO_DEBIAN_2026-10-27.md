> **Actualización 28/10/2026:** la consulta habitual de candidaturas está recuperada mediante Firefox y AT-SPI2. Véase [BC-16](RECUPERACION_INFOJOBS_ATSPI_2026-10-28.md). La parte BiDi/OAuth que sigue documenta el estado histórico, no la ruta de producción.

## Actualización de la revisión del 27/10/2026

La API de InfoJobs ha sido oficialmente deshabilitada, según respuesta de
su departamento de Privacidad recibida el 27/10/2026. El flujo OAuth descrito
en BC-14 no constituye ya una opción operativa.

La consulta nueva en Debian devolvió private_read_unverified, mientras que
una consulta anterior había recuperado **una** candidatura de ILUNION, estado
Inscrito. Por consiguiente, el resultado antiguo se conserva como histórico,
no como situación actual comprobada.

La nueva instrumentación de diagnóstico solo devuelve indicadores cerrados
de estructura de página, sin HTML, URLs completas, contraseñas ni datos del
candidato. En la segunda consulta, la ruta seguía siendo de candidaturas,
pero no aparecieron enlaces reconocibles ni las cabeceras esperadas de la
interfaz; tampoco un campo de contraseña. **Causa no determinada**:
renderizado/estructura/sesión. No atribuirlo a caducidad sin prueba.

Se ha confirmado el cierre del puerto temporal 9222. El navegador Firefox
gestiona exclusivamente una sesión autorizada; no se hace login con
credenciales personales ni se intenta eludir controles de acceso.
La lectura de Gmail y las tareas programadas en la nube no equivalen
a acceso actual a los mensajes internos de InfoJobs.

---
> **ACTUALIZACIÓN BC-14 (27/10/2026):** tras comprobar los términos oficiales
> de InfoJobs Developers, la vía de rellenar la contraseña del candidato
> desde GNOME Keyring **se deshabilita** en Buscar Curro. La integración para
> accesos nuevos debe utilizar OAuth 2.0 oficial, sin solicitar contraseñas
> personales; véase `infojobs_oauth_oficial.py` y
> [OAUTH_INFOJOBS_OFICIAL_2026-10-27.md](OAUTH_INFOJOBS_OFICIAL_2026-10-27.md).
> Los apartados siguientes describen el estado experimental BC-13 y ya no
> autorizan el uso de ese mecanismo de contraseña.

# Buscar Curro: lectura de InfoJobs mediante Firefox + almacén de llaves (BC-13)

**Estado verificado el 27/10/2026**. Ejecución exclusivamente en Debian, presupuesto
adicional 0 €, código público sin contraseñas ni datos privados.

## Arquitectura

- **Firefox de Debian**: conserva la sesión autorizada de InfoJobs en el perfil
  local `~/.local/share/buscar-curro/firefox-infojobs` con permisos 700.
- **Almacén GNOME Keyring**: colección independiente «Credenciales del laboratorio»,
  entradas `infojobs/usuario` e `infojobs/clave`; el programa
  `infojobs_keyring_client.py` verifica exclusivamente su disponibilidad y ofrece
  lectura restringida a esa colección para el programa local. Los valores no
  se imprimen, ni se aceptan por CLI/entorno, ni se suben a GitHub.
- **Lector Firefox**: `infojobs_browser_bidi.mjs` utiliza WebDriver BiDi del
  Firefox oficial para consultar el apartado privado «Mis ofertas». **No** usa
  la API privada antigua que devolvía HTTP 405. Rechaza dominios ajenos a
  `https://www.infojobs.net/` y conserva solo puesto, empresa, estado y última
  actividad observada.
- **Orquestador**: `infojobs_consulta_debian.py` abre temporalmente Firefox con
  depuración **solo en 127.0.0.1:9222**, realiza una consulta y restaura el
  navegador ordinario sin ese puerto abierto. Si detecta formulario de inicio,
  puede pedir las credenciales al llavero mediante un único proceso local y
  entregarlas al propio formulario de InfoJobs por canal local en memoria.
  **Ningún otro dominio recibe claves y no se repite el inicio de sesión.**
  Un CAPTCHA o código de doble factor sigue requiriendo intervención autorizada.

## Comprobaciones

- `python3 infojobs_keyring_client.py --estado`: almacén disponible,
  desbloqueado y dos entradas guardadas. Esta comprobación solo lee metadatos.
- `node --test test_infojobs_browser_bidi.mjs` y
  `python3 -m unittest discover -q`: pruebas locales sin secretos reales.
- **Consulta real efectuada** con Firefox de Debian: una candidatura de ILUNION
  recuperada y clasificada como «Inscrito»; **no** constituye una invitación de
  entrevista. Resultado local con permisos 600.
- El informe privado está en
  `~/.local/share/buscar-curro/infojobs_privado.json`; **no** se escribe en Git.
- Confirmado que la conexión de depuración queda cerrada al concluir.
  El Firefox normal se restaura.
- La vía experimental HTTP con credenciales almacenadas se probó una única vez
  y devolvió 405. Se retiró la opción de utilizarla desde el nuevo módulo.
- **Pendiente de verificación**: renovación automática del inicio cuando la sesión
  haya caducado, y la gestión del segundo factor; no se fuerza un cierre de sesión
  válido ni se realizan intentos de contraseña innecesarios.

## Uso

```sh
cd /home/labgestor/proyectos/Buscar-Curro
python3 infojobs_consulta_debian.py --comprobar
python3 infojobs_keyring_client.py --estado
python3 infojobs_consulta_debian.py --revisar
```

La consulta **no envía candidaturas**, no lee el correo, no altera el CV ni
programa tareas de ejecución recurrente. Requiere Debian activo y una sesión
gráfica del usuario disponible. La lectura de Gmail y el recolector público de
GitHub Actions siguen independientes y **no tienen acceso al almacén**.
No dejar habilitado permanentemente el puerto de depuración: el orquestador
lo cierra tras revisar. Las credenciales del llavero pueden ser solicitadas
por procesos del mismo usuario Linux desbloqueado: GNOME Keyring no garantiza
aislamiento estricto entre aplicaciones del mismo usuario.

## Reversión

El código se elimina con Git sin afectar las credenciales, el CV o el perfil
de Firefox; el informe privado puede retirarse sin tocar el almacén. Nunca
exportar o copiar contraseñas/cookies a la rama GitHub pública.
