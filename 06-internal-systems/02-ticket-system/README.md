# Ticket System

**Puntos:** 3 · **Estado:** resuelto y validado  
**Flag:** `FLAG{BZPL-lZ0x-JkZH-gVoD}`

## Enumeración

`http://ticket.nren.tcc` expone un osTicket. La base de conocimiento indica
que los tickets numerados del 1 al 10 pueden consultarse con el correo
corporativo correspondiente. Se probaron los usuarios que aparecen en la
documentación pública, sin adivinar la flag.

El ticket de Eve (`eve@nren.tcc`, número 2) era una incidencia ordinaria. El
ticket de Dmitri número 3, en cambio, contenía credenciales de una base de
datos de pruebas:

```text
host: db.nren.tcc
database: crmtest
user: crmtest
password: LearnHowToOptimize
```

## Acceso a la base de datos

Con esas credenciales, la base `crmtest` tenía una única tabla interesante:

```sql
SHOW TABLES;
SELECT * FROM secrets;
```

Resultado relevante:

```text
1 | flag | FLAG{BZPL-lZ0x-JkZH-gVoD}
```

La flag fue enviada y CTFd la aceptó.

## Lección

Los sistemas de help desk deben aplicar control de acceso a tickets y evitar
publicar secretos operativos en conversaciones visibles para otros usuarios.
