# Buscar Curro — currículo privado y ejecución prioritaria en Debian

**Fecha:** 2026-10-26. **Presupuesto adicional:** 0 €.

## Comprobaciones reales

- `debian-laboratorio` se encontró inicialmente apagado. Se arrancó la VM utilizando el script de recuperación ya existente. El agente remoto de Debian se recuperó sin instalar servicios ni modificar reglas globales.
- El repositorio canónico en Debian es `/home/labgestor/proyectos/Buscar-Curro`. Se conservó su árbol original migrado y se creó una rama de trabajo en el árbol existente.
- Se recuperó un PDF de CV adjunto a una candidatura del 13 de octubre de 2026 (dos páginas). Se trasladó a Linux usando Windows únicamente como **puente temporal de transferencia** y se borró la copia temporal. Se comprobaron el SHA-256 de origen/destino, tamaño, lectura PDF y permisos privados.
- El PDF está **fuera de Git**, en `~/.local/share/buscar-curro/cv_actual.pdf`, y la carpeta pertenece exclusivamente al usuario Linux (`700`, archivo `600`).
- El histórico público del recolector se obtiene con `git fetch` desde la rama `buscar-curro-resultados`; nunca contiene el CV ni se añaden credenciales al repositorio.
- `private_cv_review.py` extrae **localmente en Debian** las competencias verificables del documento con `pdftotext` y contrasta exclusivamente la información pública de los anuncios. Es deliberadamente conservador: no infiere habilitación sanitaria, colegiación, grado en Trabajo Social, FP de Integración Social ni especialidades forenses a partir de un grado general. No aplica a ofertas ni accede a cuentas personales.
- Primera prueba: 30 fichas públicas con tipo oferta examinadas, ninguna recomendación de alta prioridad una vez corregidos falsos positivos. No equivale a ausencia de plazas vigentes.
- Revisión privada en `~/.local/share/buscar-curro/revision_privada.json`, también con permiso `600`. Incluye indicación de que los anuncios están **sin validar**.

## Uso operativo en Linux (sin Windows para las tareas del programa)

```sh
cd /home/labgestor/proyectos/Buscar-Curro
python3 private_cv_review.py --refresh-public
```

El programa descarga solo JSON de la rama pública, fija el SHA del commit para todas las fuentes, extrae el perfil de `cv_actual.pdf` local, genera el análisis local y no envía datos personales a GitHub. Requiere que la VM tenga conectividad GitHub ya permitida en su entorno.

La búsqueda diaria sigue ejecutándose en **GitHub Actions, en Linux**; sus resultados son públicos, de alcance limitado, y NO contienen el CV. El nuevo comparador **se ejecuta localmente bajo demanda** y no se presenta como parte de la ejecución diaria en GitHub. Las tareas programadas de ChatGPT pueden comparar la oferta con el CV adjunto conservado en Gmail siempre que la conexión Gmail esté realmente disponible en la ejecución.

## Dependencias aún no migradas: importantes

- Debian se ejecuta en **VirtualBox sobre un anfitrión Windows**. Apagar el ordenador anfitrión apaga la VM. No afirmar autonomía física del host.
- El agente remoto Debian utiliza actualmente un **proxy restringido de salida alojado en Windows**. El proxy es distinto de ejecutar código del proyecto en Windows. La independencia de esa conexión no está verificada.
- La sesión autenticada de InfoJobs recuperada está abierta en **Chrome de Windows**, no en una sesión de navegador Debian. No copiar cookies ni credenciales entre sistemas ni saltar medidas anti-bot/2FA. Su uso en Linux exigiría una conexión autorizada del navegador Debian y nuevo inicio de sesión seguro.
- No cambiar la red de la VM, crear puentes, habilitar NAT sin auditoría ni desconectar la recuperación Windows mientras sea el último recurso operativo. La independencia física del anfitrión **no es el objetivo**: Windows sigue siendo el anfitrión de VirtualBox. Lo exigido es desarrollo y procesamiento exclusivo de Buscar Curro en Debian y GitHub Actions Linux, sin carpetas de código operativas en Windows.
- La privacidad impide publicar el CV o el perfil íntegro en la rama pública; sin una integración segura y aprobada, GitHub Actions no tiene acceso al PDF y no debe afirmar que lo emplea.

## Validación y reversión

- `python3 -m unittest discover -q` y `python3 -m py_compile private_cv_review.py`.
- `python3 private_cv_review.py --refresh-public`: procesa datos oficiales/públicos sin modificar ni enviar candidaturas.
- Verificar SHA-256 y permisos `700/600` del directorio y PDF privados, comprobar resultados en `revision_privada.json`.
- Reversión del módulo: eliminar únicamente el código nuevo o usar Git; **no borrar el currículo privado** salvo solicitud expresa.
