# Inicio de sesión legítimo de InfoJobs desde Debian — BC-11

El comando `python3 infojobs_acceso_local.py --abrir` abre **Firefox en ventana privada**, en
la **web oficial** `https://www.infojobs.net/`. El usuario pulsa «Acceso candidatos» e
introduce **él mismo** su correo, contraseña y el código 2FA cuando InfoJobs los pida.
No existe ningún formulario de credenciales dentro del programa Buscar Curro, ni lectura de
las pulsaciones, ni almacenamiento de contraseñas, cookies, tokens o códigos de verificación
por el programa. El modo privado de Firefox elimina las cookies de sesión al cerrar
las ventanas privadas. **Es un acceso interactivo, no un lector automático de mensajes.**

Se añadió el lanzador por usuario en `~/.local/share/applications/buscar-curro-infojobs.desktop`
con `python3 infojobs_acceso_local.py --instalar-lanzador`; aparece en el menú de
aplicaciones de Debian como «Buscar Curro - acceso InfoJobs». No se instala en Windows
ni añade servicio de inicio automático.

## Requisitos
- Debian debe estar arrancado y el usuario `labgestor` debe haber iniciado sesión
  en el **escritorio gráfico XFCE**, no solo por SSH/Remote Desktop Commander.
- Firefox debe estar instalado. No se instalan paquetes ni se cambia el firewall, proxy,
  NAT, VirtualBox, SSH, reglas de acceso ni configuración de red.
- Si la web muestra bloqueo 403/405, CAPTCHA o falla la conectividad, detener el intento.
  Introducir más credenciales o crear un formulario alternativo **no resuelve** ese bloqueo.

## Comprobaciones
```sh
cd /home/labgestor/proyectos/Buscar-Curro
python3 infojobs_acceso_local.py --comprobar
python3 infojobs_acceso_local.py --abrir
```
El primer comando verifica exclusivamente sesión gráfica y disponibilidad de Firefox.
El segundo abre el navegador; **no demuestra** acceso a la cuenta, listado de candidaturas
ni disponibilidad futura. A 26/10/2026 el agente remoto detectó la sesión gráfica sin
iniciar (`graphical_session_unavailable`). En intentos de HTTP anteriores, la web
respondió 405 por acceso directo, 403 mediante proxy restringido y una prueba headless
de Firefox no completó la carga. El bloqueo real solo podrá revisarse dentro de una
sesión gráfica legítima. InfoJobs documenta el requisito de 2FA por correo.

No se copiarán perfiles, cookies ni contraseñas de Windows. El antiguo cliente experimental
`infojobs_auth.py` (autenticación mediante API) **no se usa ni se activa** aquí.
La búsqueda diaria de GitHub y el seguimiento por Gmail continúan independientes.

**Coste adicional autorizado:** 0 €.
