from __future__ import annotations
import hashlib

def make_uid(title: str, link: str, published: str = "") -> str:
    payload = (title.strip() + "|" + link.strip() + "|" + (published or "").strip()).encode("utf-8")
    return hashlib.sha1(payload).hexdigest()
