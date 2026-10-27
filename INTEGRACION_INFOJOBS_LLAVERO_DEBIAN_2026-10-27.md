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
