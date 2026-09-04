import asyncio
import hashlib
import hmac
import secrets
from datetime import datetime, timedelta, timezone

from app.core.config import settings


def _hash_password(password: str) -> str:
    salt = secrets.token_hex(16)
    digest = hashlib.sha256(f"{salt}{password}".encode()).hexdigest()
    return f"{salt}${digest}"


def _verify_password(password: str, hashed: str) -> bool:
    try:
        salt, digest = hashed.split("$", 1)
    except ValueError:
        return False
    expected = hashlib.sha256(f"{salt}{password}".encode()).hexdigest()
    return hmac.compare_digest(digest, expected)


def _create_access_token(subject: str, expires_delta: timedelta | None = None) -> str:
    expire = datetime.now(timezone.utc) + (
        expires_delta or timedelta(minutes=settings.access_token_expire_minutes)
    )
    payload = f"{subject}|{int(expire.timestamp())}"
    signature = hmac.new(
        settings.secret_key.encode(),
        payload.encode(),
        hashlib.sha256,
    ).hexdigest()
    return f"{payload}.{signature}"


def _verify_access_token(token: str) -> str | None:
    try:
        payload, signature = token.rsplit(".", 1)
        expected = hmac.new(
            settings.secret_key.encode(),
            payload.encode(),
            hashlib.sha256,
        ).hexdigest()
        if not hmac.compare_digest(signature, expected):
            return None
        subject, exp = payload.split("|", 1)
        if int(exp) < int(datetime.now(timezone.utc).timestamp()):
            return None
        return subject
    except (ValueError, TypeError):
        return None


async def hash_password(password: str) -> str:
    return await asyncio.to_thread(_hash_password, password)


async def verify_password(password: str, hashed: str) -> bool:
    return await asyncio.to_thread(_verify_password, password, hashed)


async def create_access_token(subject: str, expires_delta: timedelta | None = None) -> str:
    return await asyncio.to_thread(_create_access_token, subject, expires_delta)


async def verify_access_token(token: str) -> str | None:
    return await asyncio.to_thread(_verify_access_token, token)
