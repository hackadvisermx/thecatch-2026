# They Lie to You!

**Estado:** 4/4 capítulos resueltos y validados en CTFd.  
**Puntos:** 12 (2 + 3 + 3 + 4).

La cadena se resuelve siguiendo la API de una aplicación que expone más
información de la que debería. El primer capítulo revela la documentación
OpenAPI; esa documentación descubre los endpoints administrativos que se usan
en los capítulos siguientes.

## Resultado

| Capítulo | Puntos | Flag | Evidencia |
|---|---:|---|---|
| 1 — Exploration | 2 | `FLAG{McUs-Wrjs-8MbE-SiIt}` | [`openapi.json`](01-exploration/evidence/openapi.json) |
| 2 — The Owner | 3 | `FLAG{nJd3-nn70-B55u-ld34}` | [`admin-flag.json`](02-owner/evidence/admin-flag.json) |
| 3 — Count with Me | 3 | `FLAG{Ugaa-S1zs-UwsE-uIUA}` | [`owner-address.json`](03-count-with-me/evidence/owner-address.json) |
| 4 — Hidden Information | 4 | `FLAG{EcfI-bCKg-7x4I-nYlC}` | [`owner-data.png`](04-hidden-information/evidence/owner-data.png) |

## 1. Exploration: la documentación ya contiene una flag

La web pública usa `http://api.theylietoyou.tcc`. Al solicitar
`GET /v3/api-docs` se obtiene la especificación OpenAPI completa. La flag del
primer capítulo aparece en la descripción del esquema `TokenResponse`.

La misma especificación enumera endpoints que no aparecen en la interfaz,
entre ellos `/api/admin/flag`, `/api/admin/conf`,
`/api/admin/users` y `/api/admin/users/{userId}/meta/{metaId}`. Por eso el
Chapter 1 es la pista que desbloquea el resto de la cadena; no era necesario
hacer fuzzing ni fuerza bruta.

## 2. The Owner: confusión de emisor entre producción y DEV

Las credenciales proporcionadas por el reto (`newWarrior` /
`chAng3melaTer123`) permiten obtener un JWT HS256 válido en:

```text
POST http://api.theylietoyou.tcc/api/auth/login
```

El payload legítimo contiene `role: AUTHOR` y el emisor de producción. Se
conservan el encabezado y la firma originales, pero se cambia únicamente el
payload a `role: ADMIN` y `username: admin`. Producción rechaza el token
modificado, mientras que el backend DEV acepta ese JWT emitido para producción:

```text
GET http://untraceable-dev-api.theylietoyou.tcc/api/admin/flag
Authorization: Bearer <JWT-con-payload-modificado>
```

La respuesta devuelve la flag del Chapter 2. Esto demuestra una validación
incorrecta de firma/emisor en el entorno DEV; no se intentaron contraseñas ni
se hizo enumeración agresiva.

## 3. Count with Me: calcular el `metaId`

Con el mismo token DEV se consultan `/api/admin/conf` y `/api/admin/users`.
La configuración expone la fórmula:

```text
metaId = 154700 + (userId * 1000) + fieldOffset
Address = 41
Data    = 99
```

El usuario que corresponde al propietario de la aplicación es `ermartinez`,
con `userId = 17`. Por tanto, para el campo Address:

```text
154700 + (17 * 1000) + 41 = 171741
```

La petición a `/api/admin/users/17/meta/171741` devuelve la dirección y la
flag del Chapter 3 en el mismo campo `content`.

## 4. Hidden Information: esteganografía en el campo Data

Para el campo Data se calcula `154700 + (17 * 1000) + 99 = 171799` y se
consulta `/api/admin/users/17/meta/171799`. Su contenido es un PNG RGBA
codificado en Base64. La imagen contiene además un comentario PNG que apunta a
`stegano.theylietoyou.tcc`, pero ese hostname no es necesario para resolver el
reto.

La flag está en el bit menos significativo de cada canal RGBA. La extracción
MSB-first de esos bits produce `FLAG{EcfI-bCKg-7x4I-nYlC}`. El PNG original se
conserva como [`owner-data.png`](04-hidden-information/evidence/owner-data.png)
para poder verificarlo sin depender del servicio.

## Reproducción

Desde este directorio, con conectividad al entorno del CTF:

```bash
python3 -m pip install -r requirements.txt
python3 solve.py --evidence-dir .
```

El script inicia sesión, obtiene el OpenAPI, construye el JWT modificado solo
para el backend DEV, calcula los dos `metaId`, guarda las respuestas de texto,
decodifica el PNG y comprueba la flag por LSB. No contiene las flags como
respuestas prefijadas.

## Validación en CTFd

Las cuatro respuestas fueron enviadas a CTFd y aceptadas con estado **Correct**.
La captura del último envío queda en
[`ctfd-correct.jpg`](04-hidden-information/evidence/ctfd-correct.jpg).

## Archivos conservados

| Archivo | Uso |
|---|---|
| `solve.py` | Reproducción completa de la cadena de cuatro capítulos. |
| `requirements.txt` | Dependencias mínimas (`requests`, `Pillow`). |
| `01-exploration/evidence/openapi.json` | Especificación pública que contiene la primera flag. |
| `02-owner/evidence/admin-*.json` | Respuestas DEV usadas para el token y la fórmula. |
| `03-count-with-me/evidence/owner-address.json` | Metadata Address del usuario 17. |
| `04-hidden-information/evidence/owner-data.png` | PNG RGBA original con la flag LSB. |
| `04-hidden-information/evidence/ctfd-correct.jpg` | Confirmación visual de CTFd. |
