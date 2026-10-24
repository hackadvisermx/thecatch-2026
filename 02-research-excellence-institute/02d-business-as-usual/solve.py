"""Decode the PDF's cat gazes and reveal the PNG's alpha-channel flag.

Run: python3 solve.py [--fetch]
Without --fetch, the saved PNG is used and no VPN is needed.
Optional automatic transcription requires the tesseract executable.
"""
import argparse
from io import BytesIO
import math
from pathlib import Path
import re
import shutil
import subprocess
from urllib.parse import urljoin
from urllib.request import urlopen
from zipfile import ZipFile

import pymupdf as fitz
from pypdf import PdfReader
from pypdf.generic import ContentStream
from PIL import Image

ROOT = Path(__file__).resolve().parent

# (eye position relative to each Form BBox, gaze vector in screen coordinates).
# These positions/directions were read visually from the eleven cat drawings.
# They are geometry, not a substitution alphabet: the same cat can select many
# different characters depending on where it is placed in the document.
GAZES = {
    1: (.769, .683, 0, 1),
    2: (.1805, .5316, -1, 0),
    3: (.50, .66, 0, 1),
    4: (.83, .40, 1, 0),
    5: (.7564, .1725, 1, -1),
    6: (.1695, .339, -1, 0),
    7: (.2694, .5064, 0, -1),
    8: (.25, .67, -1, 1),
    9: (.2873, .6508, 1, 1),
    10: (.75, .25, 0, -1),
    11: (.2327, .5909, -1, 0),
}


def multiply(a, b):
    return (
        a[0]*b[0]+a[1]*b[2], a[0]*b[1]+a[1]*b[3],
        a[2]*b[0]+a[3]*b[2], a[2]*b[1]+a[3]*b[3],
        a[4]*b[0]+a[5]*b[2]+b[4], a[4]*b[1]+a[5]*b[3]+b[5],
    )


def extract():
    # document.pdf is actually the original ZIP download. Read its PDF member
    # directly so the solution also works without the extracted copy on disk.
    with ZipFile(ROOT/'document.pdf') as archive:
        pdf = archive.read('document_DoHM.pdf')
    reader = PdfReader(BytesIO(pdf))
    doc = fitz.open(stream=pdf, filetype='pdf')
    cats = []
    for pi, page in enumerate(reader.pages):
        matrix = (1, 0, 0, 1, 0, 0)
        stack = []
        for args, op in ContentStream(page.get_contents(), reader).operations:
            if op == b'q':
                stack.append(matrix)
            elif op == b'Q':
                matrix = stack.pop()
            elif op == b'cm':
                matrix = multiply(tuple(float(v) for v in args), matrix)
            elif op == b'Do':
                name = str(args[0])
                obj = page['/Resources']['/XObject'][name].get_object()
                rect = fitz.Rect([float(v) for v in obj['/BBox']])
                rect = rect*fitz.Matrix(matrix)*doc[pi].transformation_matrix
                cats.append(dict(page=pi, name=name, rect=list(rect)))
    # Preserve stream order. Sorting by nearby baselines corrupts the greeting.
    return doc, cats


def decode():
    doc, cats = extract()
    page_chars = [
        [ch for block in page.get_text('rawdict')['blocks'] if 'lines' in block
         for line in block['lines'] for span in line['spans'] for ch in span['chars']]
        for page in doc
    ]
    decoded = []
    for i, cat in enumerate(cats, 1):
        ax, ay, dx, dy = GAZES[int(cat['name'][3:])]
        x0, y0, x1, y1 = cat['rect']
        eye_x, eye_y = x0+(x1-x0)*ax, y0+(y1-y0)*ay
        candidates = []
        for ch in page_chars[cat['page']]:
            if ch['c'].isspace():
                continue
            left, top, right, bottom = ch['bbox']
            vx = (left+right)/2-eye_x
            vy = (top+bottom)/2-eye_y
            along = (vx*dx+vy*dy)/math.hypot(dx, dy)
            across = abs(vx*dy-vy*dx)/math.hypot(dx, dy)
            if along > 0 and math.hypot(vx, vy) < 18:
                # Prefer characters on the gaze ray, with a small penalty for
                # distance so the first character wins over farther collinear ones.
                candidates.append((across+.08*along, ch['c']))
        if not candidates:
            raise ValueError(f'No target for cat {i}')
        candidates.sort()
        chosen = candidates[0][1]
        decoded.append(chosen)
        print(f'{i:02} p{cat["page"]+1} {cat["name"]:5} -> {chosen!r}')
    return ''.join(decoded)


def reveal_alpha(image_path):
    output = image_path.with_name(image_path.stem+'-alpha.png')
    with Image.open(image_path) as image:
        if 'A' not in image.getbands():
            raise ValueError('The image has no alpha channel')
        image.getchannel('A').save(output)
    print(f'Alpha channel: {output}')
    if not shutil.which('tesseract'):
        print('Open the alpha-channel PNG to read the flag (or install tesseract).')
        return
    result = subprocess.run(
        ['tesseract', str(output), 'stdout', '--psm', '11'],
        capture_output=True, text=True, check=True,
    )
    print(result.stdout.strip())
    match = re.search(r'FLAG\{[A-Za-z0-9-]+\}', re.sub(r'\s+', '', result.stdout))
    if match:
        print(f'\nFlag: {match[0]}')
    else:
        print('OCR did not identify a flag; inspect the alpha-channel PNG.')


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--fetch', action='store_true')
    parser.add_argument('--image', type=Path, default=ROOT/'evidence/hiddenpaws6.png')
    args = parser.parse_args()
    message = decode()
    print(f'\nMessage: {message}')
    match = re.search(r'([a-z0-9-]+\.tcc)', message)
    if match:
        url = f'http://{match[1]}/'
        print(f'URL: {url}')
        if args.fetch:
            try:
                with urlopen(url, timeout=15) as response:
                    html = response.read().decode('utf-8')
                src = re.search(r'<img\b[^>]*\bsrc=[\"\']([^\"\']+)', html)
                if not src:
                    raise ValueError('The service returned no image')
                with urlopen(urljoin(url, src[1]), timeout=15) as response:
                    data = response.read()
                args.image.parent.mkdir(parents=True, exist_ok=True)
                args.image.write_bytes(data)
            except OSError as error:
                parser.exit(1, f'Cannot reach the service; check the CTF VPN/DNS: {error}\n')
    if args.image.is_file():
        reveal_alpha(args.image)
    else:
        print('No saved PNG. Connect the CTF VPN and run again with --fetch.')


if __name__ == '__main__':
    main()
