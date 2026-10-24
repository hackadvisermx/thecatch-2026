# Internal Systems — Secure Terminal Server

Estado: **resuelto y validado** (3 puntos).

Flag: `FLAG{qPb2-qVV8-WwkZ-Kq7G}`

## Servicio

- Host: `home.nren.tcc` (`10.99.26.60`).
- TCP/22: OpenSSH `10.0p2 Debian 7+deb13u4`; solo ofrece autenticación por clave pública.
- TCP/80: Apache `2.4.68 (Debian)`.
- La raíz web solo muestra la imagen genérica “Secure Terminal Server”.

## Hallazgo

El reto describe la publicación de homepages desde el directorio personal, lo que apunta a `mod_userdir`. La enumeración de nombres de usuario reveló varios directorios publicados; `~karen/` tenía un listado de directorio especialmente interesante:

```text
/.bash_history
/.google_authenticator
/id_ed25519
/.ssh/
```

El historial de Karen mostraba dos errores de configuración:

1. La clave privada `id_ed25519` estaba publicada por la homepage.
2. Se había activado Google Authenticator y el secreto TOTP aparecía en el historial al crear el QR.

La clave se descargó solo a un archivo temporal y se eliminó al terminar. Con la clave se autenticó por SSH; el servidor solicitó el segundo factor. El TOTP se calculó a partir del secreto expuesto y se entregó al prompt de `keyboard-interactive`:

```text
[ NREN 2FA gateway ] authentication successful
FLAG{qPb2-qVV8-WwkZ-Kq7G}
```

La versión Apache `2.4.68` también es compatible con la pista técnica de `mod_userdir` y con **CVE-2026-79768**, pero no fue necesario usar el bypass `~.` para recuperar la flag: el listado de `~karen/` y la exposición de credenciales fueron suficientes.

## Comprobaciones realizadas

- Enumeración de usuarios mediante `GET /~usuario/`; `david`, `john`, `karen`, `peter` y `tom` devolvieron índices.
- Revisión recursiva del índice de `karen` y de sus archivos de shell/SSH.
- Variantes de `.`/`..`, codificación URL, segmentos redundantes y traversal controlado.
- Intento inicial de autenticación SSH con Kerberos: el servicio no ofrece GSSAPI.
- Autenticación final con `id_ed25519` + TOTP y recuperación de la flag.

## Estado

La flag quedó recuperada y validada en CTFd. No se conserva la clave privada ni el secreto TOTP en el repositorio.

