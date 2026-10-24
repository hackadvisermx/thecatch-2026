# Science Hot News

**Puntos:** 2 · **Estado:** resuelto y validado  
**Flag:** `FLAG{Qdq3-LPjI-UQog-K1Ox}`

## Descubrimiento

La pista indica que el servicio solo está disponible por la VPN. La resolución
de `science-hotnews.nren.tcc` lleva a `wp-srv.nren.tcc` (`10.99.26.62`). La
raíz HTTP solo muestra una página de reconstrucción, así que se enumeraron
archivos ocultos.

El archivo `/.wp-config.php.swp` estaba expuesto. Es un *swap file* de Vim y
puede inspeccionarse con `strings` o recuperarse con Vim. Entre su contenido
aparecía la definición de `AUTH_KEY`:

```text
define( 'AUTH_KEY', 'FLAG{Qdq3-LPjI-UQog-K1Ox}' );
```

La flag se envió y CTFd la aceptó.

## Lección

Los archivos temporales de editores pueden contener el contenido completo de
configuraciones borradas. No deben publicarse archivos `*.swp`, copias de
seguridad ni volcados de configuración en el document root.
