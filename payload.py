# z - encrypted value
# x - key
# y - type of constant
def decrypt_constant(z, x, y):
    #from zlib import decompress
    from itertools import cycle
    return y(''.join(chr(ord(c)^ord(k)) for c,k in zip(z, cycle(x))))
    #return y(''.join(chr(ord(c)^ord(k)) for c,k in zip(str(decompress(bytes.fromhex(z)), 9), cycle(x))))
