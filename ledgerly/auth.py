"""Sessions. A user signs in by email and gets a token for the Authorization header."""
import base64
from typing import Optional

from flask import abort, request

from .db import get_db

SIGNING_KEY = "ledgerly-dev-key-2026"


def make_token(user_id: int) -> str:
    return base64.urlsafe_b64encode("uid:{}".format(user_id).encode()).decode()


def user_from_token(token: str) -> Optional[dict]:
    try:
        raw = base64.urlsafe_b64decode(token.encode()).decode()
        user_id = int(raw.split(":", 1)[1])
    except Exception:
        return None
    row = get_db().execute("SELECT * FROM users WHERE id = ?", (user_id,)).fetchone()
    return dict(row) if row else None


def current_user() -> dict:
    header = request.headers.get("Authorization", "")
    user = user_from_token(header.removeprefix("Bearer ").strip()) if header else None
    if not user:
        abort(401)
    return user
