import base64


def is_base64(value: bytes | str) -> bool:
    try:
        base64.b64decode(value, validate=True)
        return True
    except Exception:
        return False


def decode(value: bytes | str) -> bytes:
    return base64.b64decode(value)
