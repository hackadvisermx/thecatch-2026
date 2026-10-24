# Document Scan

Flag validada en CTFd: `FLAG{GOTO-NREN-BALL-BABY}`.

## Resolución

1. Descargué el ZIP de evidencia indicado por el reto y verifiqué su SHA-256 (`09982464cc16f288be66d33874de8bb1db6a414503e99666d15087dc5e1f3269`). Contenía `document_scan.pcapng`, `reference_scan.pcapng` y una imagen de referencia.
2. En ambos PCAP, el flujo TCP principal era `10.10.255.11 ↔ 10.10.1.9:8610` y usaba mensajes con cabecera `MFNP`.
3. Cada respuesta del servidor contenía bloques de imagen. En los bloques grandes, los primeros 8 bytes son metadatos MFNP; concatenando el resto se obtienen exactamente `4960 × 7015 = 34,794,400` bytes de escala de grises.
4. Convertí ese buffer a una imagen de 4960×7015 y leí el QR situado al pie del documento con `zbarimg`.

```bash
tshark -r document_scan.pcapng -Y 'tcp.port==8610 && tcp.len>0' \
  -T fields -e ip.src -e tcp.seq -e tcp.payload
# reensamblar respuestas, quitar la cabecera de 8 bytes de cada bloque de imagen
convert -size 4960x7015 -depth 8 gray:document.raw document.png
zbarimg --quiet document.png
```

El QR devuelve la flag anterior.
