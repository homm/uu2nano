import uuid


alphabet = b'_-0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ'

_low_mask = 2 ** 62 - 1
_const_bits = 0b10 << 62
_alpharev = bytearray(max(c for c in alphabet) + 1)
for i, c in enumerate(alphabet):
    _alpharev[c] = i
del i, c


def uuid_to_nano(u: uuid.UUID, *, alphabet=alphabet) -> str:
    u = u.int
    assert u >> 62 & 0b11 == 2
    u = (u >> 64 << 62) | (u & _low_mask)
    b = bytearray(21)
    for i in range(21):
        b[i] = alphabet[u >> (6 * i) & 0b111111]
    return b.decode()


def nano_to_uuid(nano: str, *, alphabet=_alpharev) -> uuid.UUID:
    u = 0
    for c in nano.encode()[::-1]:
        u = (u << 6) | alphabet[c]
    u = (u >> 62 << 64) | (u & _low_mask) | _const_bits
    return uuid.UUID(int=u)
