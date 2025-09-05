# Simple MD5 implementation (Python translation of md5.c from Embench)
# Translated line by line without simplification

import ctypes

LOCAL_SCALE_FACTOR = 51
HEAP_SIZE = 2000 + 1016 + 64
MSG_SIZE = 1000
RESULT = 0x33f673b4

# Fake heap (like in C version)
heap = bytearray(HEAP_SIZE)

# Left rotation (same macro as in C)
def LEFTROTATE(x, c):
    return ((x << c) | (x >> (32 - c))) & 0xFFFFFFFF

# Global hash state
h0 = 0
h1 = 0
h2 = 0
h3 = 0


def md5(initial_msg: bytearray, initial_len: int):
    global h0, h1, h2, h3

    # Per-round shift amounts
    r = [
        7, 12, 17, 22, 7, 12, 17, 22, 7, 12, 17, 22, 7, 12, 17, 22,
        5, 9, 14, 20, 5, 9, 14, 20, 5, 9, 14, 20, 5, 9, 14, 20,
        4, 11, 16, 23, 4, 11, 16, 23, 4, 11, 16, 23, 4, 11, 16, 23,
        6, 10, 15, 21, 6, 10, 15, 21, 6, 10, 15, 21, 6, 10, 15, 21
    ]

    # Use sine-based constants
    k = [
        0xd76aa478, 0xe8c7b756, 0x242070db, 0xc1bdceee,
        0xf57c0faf, 0x4787c62a, 0xa8304613, 0xfd469501,
        0x698098d8, 0x8b44f7af, 0xffff5bb1, 0x895cd7be,
        0x6b901122, 0xfd987193, 0xa679438e, 0x49b40821,
        0xf61e2562, 0xc040b340, 0x265e5a51, 0xe9b6c7aa,
        0xd62f105d, 0x02441453, 0xd8a1e681, 0xe7d3fbc8,
        0x21e1cde6, 0xc33707d6, 0xf4d50d87, 0x455a14ed,
        0xa9e3e905, 0xfcefa3f8, 0x676f02d9, 0x8d2a4c8a,
        0xfffa3942, 0x8771f681, 0x6d9d6122, 0xfde5380c,
        0xa4beea44, 0x4bdecfa9, 0xf6bb4b60, 0xbebfbc70,
        0x289b7ec6, 0xeaa127fa, 0xd4ef3085, 0x04881d05,
        0xd9d4d039, 0xe6db99e5, 0x1fa27cf8, 0xc4ac5665,
        0xf4292244, 0x432aff97, 0xab9423a7, 0xfc93a039,
        0x655b59c3, 0x8f0ccc92, 0xffeff47d, 0x85845dd1,
        0x6fa87e4f, 0xfe2ce6e0, 0xa3014314, 0x4e0811a1,
        0xf7537e82, 0xbd3af235, 0x2ad7d2bb, 0xeb86d391
    ]

    # Initialize hash values
    h0 = 0x67452301
    h1 = 0xefcdab89
    h2 = 0x98badcfe
    h3 = 0x10325476

    # Pre-processing (padding)
    new_len = ((((initial_len + 8) // 64) + 1) * 64) - 8
    msg = bytearray(new_len + 64)
    msg[0:initial_len] = initial_msg[0:initial_len]
    msg[initial_len] = 0x80
    bits_len = (8 * initial_len) & 0xFFFFFFFF
    msg[new_len:new_len + 4] = bits_len.to_bytes(4, byteorder="little")

    # Process the message in 512-bit chunks
    for offset in range(0, new_len, 64):
        w = [int.from_bytes(msg[offset + i:offset + i + 4], "little") for i in range(0, 64, 4)]

        a, b, c, d = h0, h1, h2, h3

        for i in range(64):
            if i < 16:
                f = (b & c) | ((~b) & d)
                g = i
            elif i < 32:
                f = (d & b) | ((~d) & c)
                g = (5 * i + 1) % 16
            elif i < 48:
                f = b ^ c ^ d
                g = (3 * i + 5) % 16
            else:
                f = c ^ (b | (~d))
                g = (7 * i) % 16

            f = (f + a + k[i] + w[g]) & 0xFFFFFFFF
            a, d, c, b = d, c, b, (b + LEFTROTATE(f, r[i])) & 0xFFFFFFFF

        # Update hash values
        h0 = (h0 + a) & 0xFFFFFFFF
        h1 = (h1 + b) & 0xFFFFFFFF
        h2 = (h2 + c) & 0xFFFFFFFF
        h3 = (h3 + d) & 0xFFFFFFFF

    return (h0, h1, h2, h3)


def initialise_benchmark():
    pass


def benchmark_body(rpt, length):
    global h0, h1, h2, h3
    result = 0

    for _ in range(rpt):
        msg = bytearray(length)
        for i in range(length):
            msg[i] = i & 0xFF

        h0, h1, h2, h3 = md5(msg, length)
        result = h0 ^ h1 ^ h2 ^ h3

    return result


def warm_caches(heat):
    benchmark_body(heat, MSG_SIZE)


def benchmark():
    return benchmark_body(LOCAL_SCALE_FACTOR * 1, MSG_SIZE)


def verify_benchmark(r):
    return r == RESULT


if __name__ == "__main__":
    r = benchmark()
    print("Result:", hex(r))
    print("Verification:", verify_benchmark(r))
