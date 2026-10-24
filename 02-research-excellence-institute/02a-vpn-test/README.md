# VPN Test — Research Excellence Institute

**Categoría:** Research Excellence Institute  
**Puntos:** 1  
**Flag:** `FLAG{7JTu-5A8s-bPlH-f4rD}`

---

## 1. Descripción

> Hi Associate Researcher,
>
> nobody can work secure without VPN. You have to install and configure OpenVPN properly. Configuration file can be downloaded from CTFd's link [VPN](https://www.thecatch.cz/vpn). Your task is to activate VPN, visit the testing pages, and get your code proving your IPv4 and IPv6 readiness.
>
> Stay curious!
>
> - IPv4 testing page is available at http://yesterday.nren.tcc
> - IPv6 testing page is available at http://tomorrow.nren.tcc

> **Hint (0 pts):** https://openvpn.net/community-resources/installing-openvpn/

---

## 2. Solución

1. **Descargar el archivo de configuración OpenVPN** desde la URL autenticada de la plataforma:
   ```
   https://www.thecatch.cz/vpn
   ```
   El archivo contiene el certificado CA, el certificado de cliente y la clave privada embebidos. Se conecta al servidor `vpn.thecatch.cz:1194` por UDP.

2. **Conectar la VPN** con privilegios de root (necesario para crear la interfaz `tun`):
   ```bash
   sudo openvpn --config ctfd_ovpn.ovpn
   ```
   Al ver `Initialization Sequence Completed` la VPN está activa. Se asigna IP `10.200.0.22` y dirección IPv6 `2001:db8:ffff::1c/64`.

3. **Obtener la primera parte de la flag (IPv4)** via HTTP:
   ```bash
   curl http://yesterday.nren.tcc
   ```
   Respuesta: `Your VPN is IPv4 ready, first part of code is FLAG{7JTu-5A8s`

4. **Obtener la segunda parte de la flag (IPv6)** via HTTP sobre IPv6:
   ```bash
   curl -6 http://tomorrow.nren.tcc
   ```
   Respuesta: `Your VPN is IPv6 ready, second part of code is -bPlH-f4rD}`

5. **Concatenar** ambas partes: `FLAG{7JTu-5A8s-bPlH-f4rD}`

6. **Submitir** la flag en la plataforma → **Correct**.

---

## 3. Notas

- La VPN asigna IPs en el rango `10.200.0.0/21` y rutas hacia `10.99.0.0/16` y `10.100.0.0/16` — redes internas del CTF.
- El flag se obtiene en **dos partes**: la primera accediendo por IPv4 y la segunda por IPv6. Ambas conexiones pasan por la VPN, que soporta dual-stack.
- `curl -6` fuerza el uso de IPv6 explícitamente; sin eso curl puede usar IPv4 aunque haya conectividad v6.
- En macOS se requiere `sudo` para OpenVPN porque necesita crear la interfaz virtual `utun` (equivalente a `tun` en Linux).
- El archivo `.ovpn` es **personal** (contiene el par cert/clave del usuario autenticado en CTFd) — no compartir.

---

## 4. Referencias

- Documentación OpenVPN: https://openvpn.net/community-resources/reference-manual-for-openvpn-2-6/
- Instalación en macOS (Homebrew): `brew install openvpn`
- Writeup de ediciones anteriores de The Catch con VPN: https://github.com/search?q=thecatch+openvpn+writeup
