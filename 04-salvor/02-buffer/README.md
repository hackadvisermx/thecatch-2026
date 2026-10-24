# Chapter 2: 'Bəfər

## Acceso al host

La ejecución del capítulo 1 permitió leer `/var/lib/deploy/.ssh/deploy`. Con esa clave se accedió al foothold SSH como `deploy` (la clave privada no se guarda en este repositorio).

El supervisor mostró un proceso `/proxy/.build/proxy` escuchando en `[::]:3001` y reenviando a DSRepos en `127.0.0.1:3000`. El fuente `/proxy/proxy.c` era legible.

## Vulnerabilidad

Las peticiones `TRACE` pasan directamente a:

```c
int len = snprintf(response, BUFFER_SIZE, buffer);
```

`buffer` es texto controlado por el cliente y se usa como formato. Además, `handle_client()` copia la primera línea completa a `logbuf`; esa copia deja el texto de la petición en el área de pila que `snprintf` consume como argumentos variádicos.

## Lectura arbitraria

El argumento 44 cae sobre la copia de `logbuf`. Una petición con `TRACE %44$s`, relleno hasta el desplazamiento correcto, un byte NUL y una dirección little-endian permite leer una dirección elegida:

```text
TRACE %44$s<relleno>\0<dirección-64-bit> HTTP/1.1
```

El prefijo de `logbuf` mide 37 bytes (marca temporal de 20 y `::ffff:127.0.0.1 ` de 17), por lo que se ajustó la dirección al argumento 44. Se filtró la pila alrededor del puntero obtenido con `%16$p`; en `0x7ffe37f4dfc8` apareció:

```text
G=FLAG{LWoM-kzkO-YFUf-XGpm}
```

La flag fue enviada y aceptada por CTFd.

## Lección

Nunca se debe pasar entrada de red como formato de `printf`/`snprintf`; debe usarse `snprintf(response, BUFFER_SIZE, "%s", buffer)`. También hay que limitar y validar las copias al búfer de log.
