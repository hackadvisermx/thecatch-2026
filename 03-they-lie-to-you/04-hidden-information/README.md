# Chapter 4 — Hidden Information

**Puntos:** 4 · **Estado:** resuelto y validado  
**Flag:** `FLAG{EcfI-bCKg-7x4I-nYlC}`

Para el campo `Data`, el `metaId` es `171799`. Su contenido es un PNG RGBA en
Base64. Al leer el bit menos significativo de cada canal (R, G, B y A) y
agrupar los bits de ocho en ocho aparece la flag.

La imagen original queda en [`evidence/owner-data.png`](evidence/owner-data.png)
y la confirmación de CTFd en [`evidence/ctfd-correct.jpg`](evidence/ctfd-correct.jpg).
