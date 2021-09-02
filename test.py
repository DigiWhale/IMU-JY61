def bitstring_to_bytes(s):
    v = int(s, 2)
    b = bytearray()
    while v:
        b.append(v & 0xff)
        v >>= 8
    return bytes(b[::-1])
print(bitstring_to_bytes('01010101'))
# print((bitstring_to_bytes('11111111') << 8) | bitstring_to_bytes('0000000011000111'))