# Chapter 1 — Exploration

**Puntos:** 2 · **Estado:** resuelto y validado  
**Flag:** `FLAG{McUs-Wrjs-8MbE-SiIt}`

La API pública expone `GET /v3/api-docs`. La flag aparece en la descripción del
esquema `TokenResponse`; además, el documento enumera los endpoints
administrativos que sirven de pista para los capítulos 2–4.

La respuesta completa se conserva en [`evidence/openapi.json`](evidence/openapi.json).
La aceptación queda documentada en [`evidence/ctfd-correct.jpg`](evidence/ctfd-correct.jpg).
La reproducción está en [`../solve.py`](../solve.py).
