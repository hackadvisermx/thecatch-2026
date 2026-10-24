# The Catch 2026 — Progress Tracker

**Evento:** The Catch 2026 — organizado por CESNET  
**Plataforma:** https://www.thecatch.cz  
**Última actualización:** 2026-10-22

---

## Progreso general

| Resueltos | Total visible | Puntos obtenidos | Puntos totales visibles |
|-----------|--------------|-----------------|------------------------|
| 21        | 22           | 48              | 50                      |

---

## Retos

### 🗂 The Story

| # | Reto | Puntos | Estado | Flag | Writeup |
|---|------|--------|--------|------|---------|
| 1 | Introduction | 0 | ✅ Resuelto | `FLAG{9UL0-nAUU-VmAf-Rh10}` | [→](01-the-story/01a-introduction/README.md) |
| 6 | Promotion | 0 | ✅ Resuelto; 16 retos desbloqueados | `FLAG{sWX8-Gu1w-QNSA-kpdz}` | [→](01-the-story/01b-promotion/README.md) |

---

### 🗂 Research Excellence Institute

| # | Reto | Puntos | Estado | Flag | Writeup |
|---|------|--------|--------|------|---------|
| 2 | VPN Test | 1 | ✅ Resuelto | `FLAG{7JTu-5A8s-bPlH-f4rD}` | [→](02-research-excellence-institute/02a-vpn-test/README.md) |
| 3 | Dr. Dvorak's Document | 1 | ✅ Resuelto | `FLAG{BCjM-6SpO-HVpI-N13B}` | [→](02-research-excellence-institute/02b-dvorak-doc/README.md) |
| 4 | CRMS | 1 | ✅ Resuelto | `FLAG{eEA9-WUne-CloQ-Ofaz}` | [→](02-research-excellence-institute/02c-crms/README.md) |
| 5 | Business as Usual | 1 | ✅ Resuelto y validado | `FLAG{THIS-ISMY-SPOT-OKAY}` | [→](02-research-excellence-institute/02d-business-as-usual/README.md) |

---

### They Lie to You!

| Reto | Puntos | Estado | Flag | Writeup |
|---|---:|---|---|---|
| Chapter 1: Exploration | 2 | ✅ Resuelto y validado | `FLAG{McUs-Wrjs-8MbE-SiIt}` | [→](03-they-lie-to-you/01-exploration/README.md) |
| Chapter 2: The Owner | 3 | ✅ Resuelto y validado | `FLAG{nJd3-nn70-B55u-ld34}` | [→](03-they-lie-to-you/02-owner/README.md) |
| Chapter 3: Count with Me | 3 | ✅ Resuelto y validado | `FLAG{Ugaa-S1zs-UwsE-uIUA}` | [→](03-they-lie-to-you/03-count-with-me/README.md) |
| Chapter 4: Hidden Information | 4 | ✅ Resuelto y validado | `FLAG{EcfI-bCKg-7x4I-nYlC}` | [→](03-they-lie-to-you/04-hidden-information/README.md) |

### SALVOR

| Reto | Puntos | Estado | Flag | Writeup |
|---|---:|---|---|---|
| Chapter 1: Act-er | 3 | ✅ Resuelto y validado | `FLAG{2cgd-Jb3C-0Tib-Iol9}` | [→](04-salvor/01-act-er/README.md) |
| Chapter 2: 'Bəfər | 5 | ✅ Resuelto y validado | `FLAG{LWoM-kzkO-YFUf-XGpm}` | [→](04-salvor/02-buffer/README.md) |
| Chapter 3: Prompt | 1 | ✅ Resuelto y validado | `FLAG{dsNI-3wkY-KzHH-8sAu}` | [→](04-salvor/03-prompt/README.md) |
| Chapter 4: Raggad | 2 | ✅ Resuelto y validado | `FLAG{TSPL-Gp8P-pLPJ-YdKy}` | [→](04-salvor/04-raggad/README.md) |

### Miscellaneous

| Reto | Puntos | Estado | Flag | Writeup |
|---|---:|---|---|---|
| Document Scan | 2 | ✅ Resuelto y validado | `FLAG{GOTO-NREN-BALL-BABY}` | [→](05-miscellaneous/00-document-scan/README.md) |
| It's a Trap! | 2 | Pendiente; *tarpit* confirmado, `5666/tcp` descartado como `tcpwrapped` | | [→](05-miscellaneous/03-its-a-trap/README.md) |
| Science Hot News | 2 | ✅ Resuelto y validado | `FLAG{Qdq3-LPjI-UQog-K1Ox}` | [→](05-miscellaneous/01-science-hot-news/README.md) |
| Experimental Server | 4 | ✅ Resuelto y validado | `FLAG{u2G3-dsoj-nLGS-M9xh}` | [→](05-miscellaneous/02-experimental-server/README.md) |

### Internal Systems

| Reto | Puntos | Estado | Flag | Writeup |
|---|---:|---|---|---|
| Data Storage | 3 | ✅ Resuelto y validado | `FLAG{ShWJ-CVi0-cZ2W-7DsZ}` | [→](06-internal-systems/01-data-storage/README.md) |
| Ticket System | 3 | ✅ Resuelto y validado | `FLAG{BZPL-lZ0x-JkZH-gVoD}` | [→](06-internal-systems/02-ticket-system/README.md) |
| Secure Terminal Server | 3 | ✅ Resuelto y validado | `FLAG{qPb2-qVV8-WwkZ-Kq7G}` | [→](06-internal-systems/04-secure-terminal-server/README.md) |
| Quantum Keys Repository | 4 | ✅ Resuelto y validado | `FLAG{xQsB-mGHP-PHNC-FMMN}` | [→](06-internal-systems/03-quantum-keys-repository/README.md) |

## Resumen de técnicas usadas

| # | Reto | Técnica / Herramienta |
|---|------|-----------------------|
| 1 | Introduction | Lectura del enunciado |
| 2 | VPN Test | OpenVPN, curl IPv4/IPv6 |
| 3 | Dr. Dvorak's Document | Keyboard layout mapping (QWERTY → Dvorak), Python |
| 4 | CRMS | SMTP reverse callback, Python socket, IPv6 |
| 5 | Business as Usual | Los 28 gatos señalan caracteres con la mirada y revelan `hiddenpaws6.tcc`. La flag está escrita en el canal alfa del PNG del servicio. Python, PyMuPDF, pypdf, Pillow y Tesseract. Validado: Correct. |
| 6 | They Lie to You! — Exploration | OpenAPI público; la flag está en la descripción de `TokenResponse`. |
| 7 | They Lie to You! — The Owner | Confusión de emisor/firma JWT entre producción y DEV; endpoint administrativo expuesto. |
| 8 | They Lie to You! — Count with Me | Fórmula de `metaId` expuesta y lectura de metadata del usuario propietario. |
| 9 | They Lie to You! — Hidden Information | PNG RGBA en Base64 y extracción de bits LSB. |
| 10 | SALVOR — Act-er | React Server Components / Server Action RCE y lectura de `FLAG` del entorno. |
| 11 | SALVOR — 'Bəfər | Format string en `TRACE` del proxy C y lectura arbitraria de pila. |
| 12 | SALVOR — Prompt | Prompt injection y salida codificada en NATO. |
| 13 | SALVOR — Raggad | Prompt injection sobre RAG y salida codificada en Base64. |
| 14 | Miscellaneous — Science Hot News | Enumeración de archivos ocultos y recuperación de un `*.swp` de Vim. |
| 15 | Internal Systems — Ticket System | Acceso a tickets 1–10, credenciales expuestas y consulta MySQL. |
| 16 | Miscellaneous — Document Scan | Reensamblado del protocolo MFNP en un buffer de imagen y lectura del QR con `zbarimg`. |
| 17 | Internal Systems — Quantum Keys Repository | Cookie de permisos manipulable, traversal del gestor de archivos, análisis de `decryptor.so` y consulta del servicio de descifrado interno. |
| 18 | Internal Systems — Data Storage | Enumeración SMB pública, pistas de Kerberos, autenticación con ticket y reutilización de un keytab expuesto. |
