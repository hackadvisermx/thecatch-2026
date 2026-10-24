# Experimental Server

**Categoría:** Miscellaneous  
**Puntos:** 4  
**Estado:** resuelto y validado en CTFd  
**Flag:** `FLAG{u2G3-dsoj-nLGS-M9xh}`

## Reconocimiento

El host `x-www26-2.nren.tcc` resolvió a `10.99.26.61`. La raíz web era una
página estática, pero la enumeración de archivos encontró:

- `/.env`, con la configuración de una aplicación y la variable `FLAG=flag.txt`;
- `/i.php`, un `phpinfo()` que confirmó PHP 7.4.33, el document root
  `/var/www/public` y que no había `open_basedir` restrictivo;
- `/adminer.php`, Adminer **4.6.2**;
- `/.DS_Store`, que reveló el directorio `backup`.

## Lectura local mediante Adminer

Adminer 4.6.2 es vulnerable a **CVE-2021-43008** (también publicado como
GHSA-97h7-mf38-g9mf). Un servidor MySQL malicioso puede solicitar al cliente
PHP que lea un archivo local mediante `LOAD DATA LOCAL INFILE`.

Se levantó un listener MySQL mínimo en la IP de la VPN (`10.200.0.14:3306`) y
se inició sesión desde el formulario de Adminer apuntando a esa IP. El listener
respondió a la primera consulta con una solicitud de archivo local y guardó los
datos recibidos. El directorio `backup` estaba prohibido por HTTP, pero no por
la lectura local del cliente. La ruta que devolvió datos fue:

```text
/var/www/public/backup/flag.txt
```

Su contenido era:

```text
FLAG{u2G3-dsoj-nLGS-M9xh}
```

La flag se envió al reto **Experimental Server** y CTFd mostró **Correct**.

## Lecciones

- No exponer `.env`, `phpinfo()` ni artefactos de macOS en producción.
- Mantener Adminer actualizado y desactivar `local_infile` cuando no sea
  necesario.
- Las reglas HTTP que bloquean un directorio no protegen los archivos frente a
  una vulnerabilidad de lectura local del proceso.
