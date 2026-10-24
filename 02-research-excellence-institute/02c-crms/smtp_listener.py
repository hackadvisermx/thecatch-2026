#!/usr/bin/env python3
"""
Minimal SMTP listener en IPv6 puerto 2525.
Imprime todo el correo recibido por stdout.
"""
import socket, threading

def handle(conn, addr):
    print(f"[+] Conexión de {addr}")
    conn.send(b"220 listener SMTP\r\n")
    body = []
    in_data = False
    while True:
        data = conn.recv(4096)
        if not data:
            break
        line = data.decode(errors="replace")
        print("RECV:", repr(line))
        cmd = line.strip().upper()
        if cmd.startswith("EHLO") or cmd.startswith("HELO"):
            conn.send(b"250 Hello\r\n")
        elif cmd.startswith("MAIL FROM"):
            conn.send(b"250 OK\r\n")
        elif cmd.startswith("RCPT TO"):
            conn.send(b"250 OK\r\n")
        elif cmd == "DATA":
            conn.send(b"354 Send data\r\n")
            in_data = True
        elif in_data and line.strip() == ".":
            conn.send(b"250 OK\r\n")
            in_data = False
        elif cmd.startswith("QUIT"):
            conn.send(b"221 Bye\r\n")
            break
        else:
            conn.send(b"250 OK\r\n")
    conn.close()

s = socket.socket(socket.AF_INET6, socket.SOCK_STREAM)
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
s.bind(("::", 2525))
s.listen(1)
print("[*] Escuchando en puerto 2525 (IPv6)...")
conn, addr = s.accept()
handle(conn, addr)
s.close()
