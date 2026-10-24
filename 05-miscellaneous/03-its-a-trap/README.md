# Miscellaneous — It's a Trap!

Estado: **pendiente de flag** (2 puntos).

## Pista confirmada

La documentación enlazada por el reto es el artículo de CESNET sobre LaBrea. LaBrea funciona como *tarpit*: responde al establecimiento TCP en direcciones/puertos no utilizados y mantiene las conexiones abiertas con una ventana de recepción mínima. Por eso un escáner TCP normal informa de una subred llena de puertos abiertos.

## Trabajo realizado

- Rango comprobado: `10.100.26.0/24` a través de la VPN. La dirección `.1` es accesible para algunos puertos, aunque `80/tcp` devuelve `Network is down` desde la ruta de la VPN.
- Se enviaron peticiones HTTP de aplicación, no solo comprobaciones de TCP.
- Se probaron los puertos web habituales y los 1.000 puertos TCP con mayor frecuencia de Nmap en las 253 direcciones utilizables: **253.000 combinaciones**.
- La clasificación mediante `TCP_CONNECTION_INFO` confirmó la firma del tarpit (ventana anunciada `snd_wnd=3`). Solo `10.100.26.1`, `.10` y `.66` mostraron una pila normal en `22/tcp`.
- En esos tres hosts se revisaron 210 puertos registrados como web/alternativos. El único puerto adicional con ventana normal fue `5666/tcp`; Nmap lo identifica como `tcpwrapped` y una petición HTTP se cierra/se resetea, por lo que no es el servicio web del reto.
- No apareció ninguna respuesta HTTP, banner ni certificado TLS que distinguiera un servicio real del *tarpit*.

## Conclusión provisional

El hallazgo todavía no está identificado. La pista sí está validada: los estados `open` del escáner son señuelos y la búsqueda debe clasificar la respuesta de aplicación (o las características TCP) antes de enviar una flag. No se envió ningún intento de flag para este reto.

