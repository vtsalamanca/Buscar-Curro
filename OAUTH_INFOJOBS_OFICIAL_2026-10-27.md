# BC-14 — conexión oficial a InfoJobs desde Debian

> **CIERRE DEL PROVEEDOR (27/10/2026):** respuesta por correo del
> departamento de Privacidad de InfoJobs: la API para desarrolladores
> ya no está disponible y, por el momento, no se prevé reactivarla.
> El formulario Manage Apps tampoco permite nuevas altas.
> **Por tanto, el procedimiento OAuth descrito más abajo es histórico y
> actualmente INVIABLE**; no solicitar Client ID/Secret ni pedir al
> usuario que complete pasos que InfoJobs ya no admite.
> El código se conserva solo como artefacto técnico inactivo. No usar
> endpoints no documentados, credenciales del candidato ni soluciones
> de pago como sustitución.


Referencia del proveedor:
- https://developer.infojobs.net/documentation/quick-start/index.xhtml
- https://developer.infojobs.net/documentation/user-oauth2/index.xhtml
- https://developer.infojobs.net/legal/legal/terms-of-use.xhtml

## Decisión
InfoJobs Developers exige OAuth 2.0 para que una aplicación acceda a los
datos privados del candidato. La aplicación cliente no debe pedir su email
y contraseña personales. El experimento BC-13 que extraía claves del llavero
para rellenar automáticamente el formulario ha quedado deshabilitado.
Se conserva el acceso de solo lectura mediante la sesión ya autorizada de
Firefox; se mantienen intactos el llavero, Firefox y Windows.

## Aplicación preparada en Debian
`python3 infojobs_oauth_oficial.py --abrir`

El escritorio dispone del acceso «Buscar Curro - conexion oficial».
GTK3 permite abrir el portal de desarrolladores, guardar credenciales
de aplicación (Client ID y Client Secret) en GNOME Keyring, solicitar
consentimiento OAuth, introducir exclusivamente el código de autorización
facilitado por InfoJobs y canjearlo por tokens OAuth en el endpoint oficial.

La API documenta `GET /api/1/application` para candidaturas (scope
`my_applications`) y `GET /api/3/application/{id}/timeline` para eventos
(scope `application_timeline`). La primera implementación incluye consulta
de una página de candidaturas y su último evento; no realiza POST de
inscripción ni modifica datos del perfil.

## Estado verificado
- Developer homepage y login HTTP 200; API de candidaturas HTTP 401 sin token.
- Implementación Python local preparada y probada con datos sintéticos.
- **No existe aún un Client ID/Client Secret registrado para Buscar Curro.**
- No se ha completado autorización OAuth ni se ha comprobado el coste
  operativo/condiciones de registro del desarrollador en la cuenta.
- La documentación pública del proveedor incluye condiciones fechadas en
  noviembre de 2012; es imprescindible validar el flujo real y la vigencia
  de los permisos desde el portal antes de afirmar que se puede usar.
- El redirect para escritorio que documenta InfoJobs usa HTTP, y el
  parámetro state generado no está validado en el retorno manual de código.
  Preferir callback HTTPS/loopback solo cuando InfoJobs confirme admitirlo.
- No se han transmitido ni leído contraseñas reales durante esta preparación.

## Bloqueo real y pasos restantes
1. Registro en el portal oficial de desarrolladores con la cuenta propia
   y aprobación explícita de términos, verificando que no implica pagos.
2. Obtener credenciales de la app y registrarlas localmente en la ventana
   de Debian, nunca en el chat, en comandos ni en GitHub.
3. Abrir el consentimiento de InfoJobs, aprobar los scopes necesarios,
   obtener/canjear el código y verificar la consulta de candidaturas.
4. Si no hay registro disponible, mantener lectura de sesión Firefox y
   Gmail; no reactivar password grant, API interna ni saltarse 2FA.

Presupuesto adicional autorizado: 0 €.
