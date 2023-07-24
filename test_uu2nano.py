import uuid
from functools import wraps

import pytest

from uu2nano import _make_alpharev, fix_uuid, nanoid_to_uuid, uuid_to_nanoid


# Try tests with random inputs multiple times
def repeat(times):
    def wrapper(fn):
        @wraps(fn)
        def inner(*args, **kwargs):
            for _ in range(times):
                fn()
        return inner
    return wrapper


def test_uuid_to_nanoid():
    nano = uuid_to_nanoid(uuid.uuid4())
    assert isinstance(nano, str)
    assert len(nano) == 21


def test_nanoid_to_uuid():
    nano = uuid_to_nanoid(uuid.uuid4())
    uu = nanoid_to_uuid(nano)
    assert isinstance(uu, uuid.UUID)


def test_stability():
    uu = uuid.UUID('492b6acb-05c7-4914-b139-253070a085e9')
    nano = uuid_to_nanoid(uu)
    assert nano == 'ggHEMKl5gfh2T7h-KC6lD'


@repeat(64)
def test_custom_alphabet():
    alphabet = b'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789[]'
    alpharev = _make_alpharev(alphabet)
    uu = uuid.uuid4()
    nano = uuid_to_nanoid(uu, alphabet=alphabet)

    # Shouldn't match with default alphabet
    assert nano != uuid_to_nanoid(uu)

    # Shouldn't match with default alpharev
    assert uu != nanoid_to_uuid(nano)

    # Should match with right reverse alphabet
    assert uu == nanoid_to_uuid(nano, alpharev=alpharev)


@pytest.mark.parametrize("bits", [0b00, 0b01, 0b11])
def test_fix_uuid(bits):
    # Reset 62-63 bits and set required bits
    uu = uuid.uuid4().int & ~(0b11 << 62) | bits << 62
    uu = uuid.UUID(int=uu)
    with pytest.raises(AssertionError, match="compliant UUID"):
        uuid_to_nanoid(uu)
    uu = fix_uuid(uu)
    nano = uuid_to_nanoid(uu)
    assert uu == nanoid_to_uuid(nano)


@repeat(64)
def test_uuid1():
    uu = uuid.uuid1()
    nano = uuid_to_nanoid(uu)
    assert uu == nanoid_to_uuid(nano)


@repeat(64)
def test_uuid3():
    ns = uuid.uuid4()
    uu = uuid.uuid3(ns, str(uuid.uuid4()))
    nano = uuid_to_nanoid(uu)
    assert uu == nanoid_to_uuid(nano)


@repeat(64)
def test_uuid4():
    uu = uuid.uuid4()
    nano = uuid_to_nanoid(uu)
    assert uu == nanoid_to_uuid(nano)


@repeat(64)
def test_uuid5():
    ns = uuid.uuid4()
    uu = uuid.uuid5(ns, str(uuid.uuid4()))
    nano = uuid_to_nanoid(uu)
    assert uu == nanoid_to_uuid(nano)
