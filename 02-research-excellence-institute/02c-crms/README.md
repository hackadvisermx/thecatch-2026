# CRMS — Research Excellence Institute

**Categoría:** Research Excellence Institute  
**Puntos:** 1  
**Flag:** `FLAG{eEA9-WUne-CloQ-Ofaz}`

---

## 1. Descripción

> Hi Associate Researcher,
>
> cats are valued members of the NREN-TCC community. Their curiosity, intelligence, and dedication help advance science, research, and education. Always eager to assist, these furry colleagues work tirelessly to support everyone—one paw, one discovery, and one helpful message at a time.
>
> "Need help? Just ask the NREN cat team. For example, they have recently created a new service called CRMS", says the Head of the Department of Feline Research.
>
> Stay curious!
>
> Access the service at http://crms.nren.tcc/

> **Hint 1 (0 pts):** All services in `nren.tcc` domain are accessible via VPN only.
>
> **Hint 2 (0 pts):** Specialists from the Department of Feline Research have discovered that experimental message reception does not require complex infrastructure. A small test mail server is just as effective for the task.

---

## 2. Solución

### Exploración inicial

El servicio (accesible solo por VPN) es una web llamada **Cat Reverse Mail Service**. Tiene un único botón que hace `POST /send`. Al pulsarlo sin listener, la respuesta revela el mecanismo:

```
IP address: 2001:db8:ffff::1c  Port: TCP/2525  Error: [Errno 111] Connection refused
```

El servidor **llama de vuelta al cliente** (nuestra IP de VPN) en el puerto **2525** para entregarle un correo vía **SMTP**. La flag viene dentro del cuerpo del email.

### Pasos

1. **Verificar la IP de VPN asignada** (debe ser `2001:db8:ffff::1c`):
   ```bash
   ifconfig utun5 | grep inet6
   ```

2. **Levantar un listener SMTP en el puerto 2525 (IPv6)**:
   ```bash
   python3 smtp_listener.py
   ```
   O con netcat (no responde al protocolo pero basta si el servidor es permisivo):
   ```bash
   nc -6 -l 2525
   ```

3. **Disparar el envío** (en otra terminal):
   ```bash
   curl -X POST http://crms.nren.tcc/send
   ```

4. El servidor CRMS conecta a `2001:db8:ffff::1c:2525` y entrega el email:
   ```
   From: Tiger the Cat <tigercat@dfr.nren.tcc>
   To: my favorite player

   Hello hooman,

   I'm sending you a secret code, to make you happy.

   FLAG{eEA9-WUne-CloQ-Ofaz}

   Do not share it with dogs!
   ```

5. **Submitir** la flag → **Correct**.

---

## 3. Notas

- **CRMS = Cat Reverse Mail Service** — el nombre es un juego con CRM (Customer Relationship Management).
- El patrón es un **callback / reverse connection**: el servidor se conecta al cliente, no al revés. Técnica común en CTFs (también en pentesting: reverse shells, SSRF con callback, etc.).
- El protocolo usado es **SMTP** (puerto 2525, alternativo al estándar 25). Requiere responder correctamente al handshake (`220`, `250`, `354`, etc.) para que el servidor entregue el mensaje.
- En macOS, `nc -6 -l 2525` puede no responder al protocolo SMTP y hacer que el servidor desconecte antes de enviar el cuerpo. El script Python `smtp_listener.py` resuelve esto.
- La IP de callback es la asignada por la VPN (`2001:db8:ffff::1c`) — diferente sesión = diferente IP.

---

## 4. Referencias

- RFC 5321 — SMTP: https://www.rfc-editor.org/rfc/rfc5321
- Puerto 2525 (SMTP alternativo): https://www.mailersend.com/blog/smtp-port
- Técnica de reverse callback en CTFs: https://ctf-wiki.org/reverse/

---

## Artefactos

| Archivo | Descripción |
|---------|-------------|
| `smtp_listener.py` | Script Python — servidor SMTP mínimo en IPv6:2525 |
