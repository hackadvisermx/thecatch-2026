# Chapter 3 — Count with Me

**Puntos:** 3 · **Estado:** resuelto y validado  
**Flag:** `FLAG{Ugaa-S1zs-UwsE-uIUA}`

`/api/admin/conf` revela `metaId = 154700 + (userId * 1000) + fieldOffset` y
`Address = 41`. El propietario identificado en `/api/admin/users` es
`ermartinez` (`userId=17`), así que el `metaId` de Address es `171741`. La
respuesta contiene la flag junto con la dirección.

Respuesta conservada: [`evidence/owner-address.json`](evidence/owner-address.json).
