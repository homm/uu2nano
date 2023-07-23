import uuid


__version__ = '1.0'

alphabet = b'_-0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ'

_low_mask = 2 ** 62 - 1
_const_bits = 0b10 << 62
_alpharev = bytearray(max(c for c in alphabet) + 1)
for i, c in enumerate(alphabet):
    _alpharev[c] = i
del i, c


def uuid_to_nanoid(uu: uuid.UUID, *, alphabet=alphabet) -> str:
    uu = uu.int
    assert uu >> 62 & 0b11 == 2, "Wrong mark bits. Use fix_uuid() for true random input"
    uu = (uu >> 64 << 62) | (uu & _low_mask)
    b = bytearray(21)
    for i in range(21):
        b[20 - i] = alphabet[uu >> (6 * i) & 0b111111]
    return b.decode()


def nanoid_to_uuid(nano: str, *, alphabet=_alpharev) -> uuid.UUID:
    uu = 0
    for c in nano.encode():
        uu = (uu << 6) | alphabet[c]
    uu = (uu >> 62 << 64) | (uu & _low_mask) | _const_bits
    return uuid.UUID(int=uu)


def fix_uuid(uu: uuid.UUID) -> uuid.UUID:
    uu = uu.int & ~(0b11 << 62) | _const_bits
    return uuid.UUID(int=uu)
