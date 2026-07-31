"""
JWT utilities: creation and decoding of access tokens.
Configuration is read from app.core.config.Settings (no hardcoded values).
"""

from datetime import datetime, timezone, timedelta
from typing import Dict

from jose import jwt, JWTError

from app.core.config import settings


def create_access_token(data: Dict[str, str]) -> str:
    """
    Create a signed JWT access token with an expiration claim.

    Args:
        data (dict): Payload data to include in the token. Must contain at least "sub".

    Returns:
        str: Encoded JWT string.
    """
    # Salin payload agar tidak memodifikasi input asli
    to_encode = data.copy()

    # Waktu kedaluwarsa ditambahkan sebagai claim "exp" (UTC)
    expire = datetime.now(timezone.utc) + timedelta(minutes=settings.access_token_expire_minutes)
    to_encode.update({"exp": expire})

    # Encode dengan kunci rahasia dan algoritma dari Settings
    encoded_jwt = jwt.encode(to_encode, settings.secret_key, algorithm=settings.algorithm)
    return encoded_jwt


def decode_access_token(token: str) -> Dict[str, str]:
    """
    Decode and verify a JWT access token.

    Args:
        token (str): The JWT string to decode.

    Returns:
        dict: The decoded payload if the token is valid.

    Raises:
        JWTError: If the token is invalid, expired, or signature verification fails.
    """
    try:
        payload = jwt.decode(token, settings.secret_key, algorithms=[settings.algorithm])
        return payload
    except JWTError as e:
        # Lempar exception agar pemanggil dapat menanganinya
        raise JWTError(f"Token tidak valid: {e}")



if __name__ == "__main__":
    # Payload uji
    test_payload = {"sub": "admin@example.com"}

    # Generate token
    token = create_access_token(test_payload)
    print(f"Token JWT:\n{token}\n")

    # Decode token
    try:
        decoded = decode_access_token(token)
        print("Payload berhasil di-decode:")
        print(decoded)
        print(f"\n'sub' sesuai: {decoded.get('sub') == test_payload['sub']}")
    except Exception as e:
        print(f"Error saat decode: {e}")    