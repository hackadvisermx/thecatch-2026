# Quantum Keys Repository

**Categoría:** Internal Systems  
**Puntos:** 4  
**Flag:** `FLAG{xQsB-mGHP-PHNC-FMMN}`

## Reconocimiento

El servicio estaba publicado en:

```text
http://quantum-keys-repository.nren.tcc
```

El primer acceso es un formulario de login. La pista indica que el usuario es
`admin` y que la política de contraseña usa el nombre de login, un carácter
especial y un número. La combinación válida fue:

```text
admin / admin#1234
```

## Escalada de permisos y lectura arbitraria

Después del login, la aplicación entrega la cookie:

```http
permissions=user
```

El servidor confía únicamente en ese valor para autorizar el repositorio. Al
cambiarlo a `permissions=admin`, se habilita `?section=repository`.

El gestor de archivos acepta `dir` sin restringirlo a la raíz pública. Con
traversal se puede listar el directorio secreto:

```text
system.php?section=repository&dir=/var/www/html/public/../secret
```

Ahí aparece `flag.inc.php`. La descarga se realiza con el mismo gestor:

```text
system.php?section=repository&dir=/var/www/html/public/../secret&download=flag.inc.php
```

El archivo contiene una llamada a una extensión PHP propia:

```php
decrypt_payload("ARnzLEyOBzP8Nid50h3l3/wsVvkrqY90fsGXUWeMKo2J47MxAgOVwUwAN8g9hHZMESMfRr96WcYPnoZoJrVttLYtRrDqlH2WqlzvmgiazuUoH6+1faHFt8N7L5iTKK2vuW/XUjtIScFqA9x8fAOXAZxwiz9rNBw0gIE/bXDptsHnr5fh0HTn");
```

## Funcionamiento de `decrypt_payload`

La propia lectura arbitraria permite recuperar el módulo
`decryptor.so` y analizar sus cadenas. El módulo revela que la función:

1. envía el ciphertext por `POST` como `data=...`;
2. añade `X-Operator-Key: C7u1EVybH9YtCyphbi73yqvUndSYHkUqzkQdnbWHjkY`;
3. usa `http://coolhacker124.tcc:5005/decrypt`;
4. evalúa la respuesta recibida como código PHP.

El host interno resolvía a `10.99.26.124`. Consultando ese endpoint con la
clave del módulo y el ciphertext del archivo se obtiene:

```php
echo "SECURITY POLICY: CODE EXECUTION DISABLED"; exit;
$flag = "FLAG{xQsB-mGHP-PHNC-FMMN}"; echo $flag;
```

El `exit` explica por qué el include normal solo muestra el mensaje de
política; la flag queda en el código descifrado que devuelve el servicio.

## Lecciones

- No usar una cookie controlada por el cliente como control de autorización.
- Canonicalizar y validar rutas antes de usar `scandir`, `filesize` o lecturas.
- No concatenar entradas del usuario con rutas de inclusión ni permitir traversal.
- No guardar secretos bajo rutas accesibles por un gestor de archivos web.
- Una extensión que evalúa respuestas remotas convierte la cadena de confianza
  en una superficie de ejecución de código.

