# Chapter 2 — The Owner

**Puntos:** 3 · **Estado:** resuelto y validado  
**Flag:** `FLAG{nJd3-nn70-B55u-ld34}`

Se obtiene un JWT legítimo con las credenciales del reto. Se conserva su firma,
pero se modifica el payload (`role=ADMIN`, `username=admin`). El backend DEV
acepta el token emitido por producción y permite consultar
`/api/admin/flag`; producción rechaza el mismo token modificado.

La respuesta y la configuración quedan en [`evidence/`](evidence/). La
reproducción está en [`../solve.py`](../solve.py).
