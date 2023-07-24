import uuid


__version__ = '1.0'


def _make_alpharev(alphabet):
    alpharev = bytearray(max(c for c in alphabet) + 1)
    for i, c in enumerate(alphabet):
        alpharev[c] = i
    return bytes(alpharev)


ALPHABET = b'_-0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ'
ALPHAREV = _make_alpharev(ALPHABET)
_LOW_MASK = 2 ** 62 - 1
_CONST_BITS = 0b10 << 62


def uuid_to_nanoid(uu: uuid.UUID, *, alphabet=ALPHABET) -> str:
    uu = uu.int
    assert uu >> 62 & 0b11 == 2, "Not RFC 4122 compliant UUID"
    uu = (uu >> 64 << 62) | (uu & _LOW_MASK)
    b = bytearray(21)
    for i in range(21):
        b[20 - i] = alphabet[uu >> (6 * i) & 0b111111]
    return b.decode()


def nanoid_to_uuid(nano: str, *, alpharev=ALPHAREV) -> uuid.UUID:
    uu = 0
    for c in nano.encode():
        uu = (uu << 6) | alpharev[c]
    uu = (uu >> 62 << 64) | (uu & _LOW_MASK) | _CONST_BITS
    return uuid.UUID(int=uu)


def fix_uuid(uu: uuid.UUID) -> uuid.UUID:
    uu = uu.int & ~(0b11 << 62) | _CONST_BITS
    return uuid.UUID(int=uu)
