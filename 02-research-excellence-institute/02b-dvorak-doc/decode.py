#!/usr/bin/env python3
"""
Convierte texto escrito con muscle memory Dvorak en teclado QWERTY
de vuelta al texto original.
"""

rows_qw = [
    "`1234567890-=",
    "qwertyuiop[]\\",
    "asdfghjkl;'",
    "zxcvbnm,./",
]
rows_dv = [
    "`1234567890[]",
    "',.pyfgcrl/=\\",
    "aoeuidhtns-",
    ";qjkxbmwvz",
]
rows_qw_s = [
    "~!@#$%^&*()_+",
    "QWERTYUIOP{}|",
    'ASDFGHJKL:"',
    "ZXCVBNM<>?",
]
rows_dv_s = [
    "~!@#$%^&*(){}",
    '"<>PYFGCRL?+|',
    "AOEUIDHTNS_",
    ":QJKXBMWVZ",
]

mapping = {}
for rq, rd in zip(rows_qw, rows_dv):
    mapping.update(zip(rq, rd))
for rq, rd in zip(rows_qw_s, rows_dv_s):
    mapping.update(zip(rq, rd))

if __name__ == "__main__":
    import sys
    text = sys.stdin.read() if len(sys.argv) < 2 else open(sys.argv[1]).read()
    print(''.join(mapping.get(ch, ch) for ch in text))
