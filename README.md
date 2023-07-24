# uu2nano

Simple tool for converting well-known [UUID](https://datatracker.ietf.org/doc/html/rfc4122)
format (36 chars) to [nanoid](https://pypi.org/project/nanoid/) format (21 chars).


## Details of conversion

UUID is basically a 128-bit number. Some of those bits contain metadata including
the version, on which the content of the remaining bits depends.
For example, for UUIDv4 all 122 unspecified bits should contain random entropy.
But more interesting that regardless of version, 2 bits in each UUID are fixed.
That is why any UUID of any version could be encoded as 126 bits.

UUIDs are encoded in hex format (4 bit per symbol) and 4 hyphens are added
as separators, which leads to 128/4 + 4 = 36 characters in the string representation.

For example: `492b6acb-05c7-4914-b139-253070a085e9`

Nanoid is encoded using 64 URL-safe symbols (`A-Za-z0-9_-`) which makes possible
to store 6 bits of information per symbol. To store 126 UUID bits, only 
126 / 6 = 21 characters are used in the string representation.

For example: `ggHEMKl5gfh2T7h-KC6lD`


## Usage

Convert one to another:

```python
import uuid
from uu2nano import fix_uuid, nanoid_to_uuid, uuid_to_nanoid

uu = uuid.uuid4()
nano = uuid_to_nanoid(uu)
assert uu == nanoid_to_uuid(nano)
```

If you receive not compliant UUIDs from third parties, there is a chance that eventually
two reserved fixed bits could be wrong. In this case `uuid_to_nanoid` will fail:

```python

@app.post
def find_book(uu: uuid.UUID):
    nano = uuid_to_nanoid(uu)

AssertionError: Wrong mark bits. Use fix_uuid() for true random input
```

If this happens you can use `fix_uuid` function to get a valid UUID.
Please note that in this case UUID will be changed, so you have to save
new alias somewhere (in UUID, int, or nanoid format).
