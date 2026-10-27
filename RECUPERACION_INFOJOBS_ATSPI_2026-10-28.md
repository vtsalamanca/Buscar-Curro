# BC-16 — InfoJobs por accesibilidad de Firefox en Debian (28/10/2026)

## Resultado comprobado
- Se recuperó el acceso legítimo a InfoJobs **desde Firefox ESR normal** en Debian; la sesión se autenticó de forma interactiva por el titular.
- La página privada de candidaturas mostró resultados reales y fue leída con la interfaz local **AT-SPI2** de Firefox, no con WebDriver/CDP ni con la API oficial (deshabilitada).
- Ruta estable en la misma máquina: `python3 infojobs_consulta_debian.py --revisar`. Devuelve JSON con `status=private_read_verified` y datos minimizados de las candidaturas visibles.
- El resultado se guarda en `~/.local/share/buscar-curro/infojobs_privado.json` con modo **0600** dentro de un directorio modo **0700**, fuera del repositorio público.
- La prueba real devolvió una candidatura activa, estado `Inscrito`. La empresa había gestionado CVs recientemente; este dato **no demuestra** lectura del CV individual.
- También se verificó visualmente que el apartado de candidaturas ocultas estaba vacío en esta sesión. El lector automático no afirma por sí mismo cubrir otros tipos de mensajes ni bandejas ajenas.
- Se completaron seis pruebas locales unitarias del extractor (tarjetas, exclusión de recomendaciones, rechazo de estados desconocidos, permisos y symlinks) y cinco del orquestador compatible con la nueva ruta; la prueba real también funcionó.

## Causa y corrección
Los intentos anteriores de leer la página con WebDriver BiDi/depuración ocasionaron fallos `private_read_unverified`, tiempo de espera y respuestas HTTP 405 asociadas a pantallas de comprobación. **Un error 405 del cliente automatizado no prueba que se haya bloqueado la cuenta del usuario.**

El Firefox ESR 153.5.0esr normal sí carga la web. Activando la interfaz accesible **solo en el proceso local**:

```bash
MOZ_ACCESSIBILITY_ATK2=1 GNOME_ACCESSIBILITY=1 GTK_MODULES=gail:atk-bridge \
  firefox --no-remote --profile "$HOME/.local/share/buscar-curro/firefox-infojobs" https://www.infojobs.net/
```

La interfaz local AT-SPI2 permitió pulsar botones oficiales, rechazar cookies adicionales y navegar por el portal de la misma forma que un usuario. No usa contraseñas, cookies ni cabeceras copiadas: la sesión la mantiene Firefox.

## Lectura diaria, requisitos y limitaciones
1. El navegador dedicado debe estar **ya abierto y autenticado**, con accesibilidad activada. No reinstalar ni cerrar su perfil para cada consulta.
2. Ejecutar `python3 infojobs_consulta_debian.py --revisar` en Debian. La ruta habitual **ya no reinicia Firefox ni abre puerto 9222**.
3. `status=private_read_verified` confirma que se encontró el documento real de «Mis candidaturas», se pudieron extraer las tarjetas y se guardó el informe privado. `private_read_unverified` no confirma ausencia de inscripciones.
4. El extractor admite estados reconocidos (`Inscrito`, `CV leído`, `Preseleccionado`, etc.) y excluye las ofertas recomendadas que aparecen dentro de las tarjetas. Si cambian la interfaz o los estados, el lector falla de forma conservadora. **No detecta todavía ni mensajes independientes ni candidaturas ocultas**.
5. Los controles de seguridad, verificación de identidad y 2FA deben completarse mediante la web oficial; no eludirlos.
6. Coste adicional 0 €. No se han publicado datos del perfil ni credenciales.

## Archivo de integración
`infojobs_lector_accesible.py` expone el lector con pruebas `test_infojobs_lector_accesible.py`. El punto de entrada existente `infojobs_consulta_debian.py --revisar` delega en él. Las funciones históricas BiDi se conservan solo como código de diagnóstico y regresión; no se ejecutan desde la opción habitual.

## Riesgos pendientes
- Persistencia del login depende de Firefox y del proveedor, no del llavero.
- Si se produce un cierre real de sesión, se requerirá autenticación legítima.
- Estados y mensajes adicionales del portal no se han demostrado ni se anuncian cubiertos.
- La periodicidad de lectura solo funciona cuando el dispositivo Debian y su sesión gráfica están disponibles; un GitHub Action público no puede leer directamente este navegador privado.
