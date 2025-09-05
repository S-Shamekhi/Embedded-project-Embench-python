#
# This file is a pure Python implementation of the SHA-256 algorithm,
# translated from the C code provided in the nettle-sha256 Embench benchmark.
# THIS IS THE CORRECTED VERSION.
#

# --- Constants and Initial Values ---

# This scale factor will be changed to equalize the runtime of the benchmarks.
CPU_MHZ = 100
LOCAL_SCALE_FACTOR = 475

SHA256_DIGEST_SIZE = 32
SHA256_BLOCK_SIZE = 64
_SHA256_DIGEST_LENGTH = 8

# SHA-256 Constants: Round constants K[0...63]
K = [
    0x428a2f98, 0x71374491, 0xb5c0fbcf, 0xe9b5dba5,
    0x3956c25b, 0x59f111f1, 0x923f82a4, 0xab1c5ed5,
    0xd807aa98, 0x12835b01, 0x243185be, 0x550c7dc3,
    0x72be5d74, 0x80deb1fe, 0x9bdc06a7, 0xc19bf174,
    0xe49b69c1, 0xefbe4786, 0x0fc19dc6, 0x240ca1cc,
    0x2de92c6f, 0x4a7484aa, 0x5cb0a9dc, 0x76f988da,
    0x983e5152, 0xa831c66d, 0xb00327c8, 0xbf597fc7,
    0xc6e00bf3, 0xd5a79147, 0x06ca6351, 0x14292967,
    0x27b70a85, 0x2e1b2138, 0x4d2c6dfc, 0x53380d13,
    0x650a7354, 0x766a0abb, 0x81c2c92e, 0x92722c85,
    0xa2bfe8a1, 0xa81a664b, 0xc24b8b70, 0xc76c51a3,
    0xd192e819, 0xd6990624, 0xf40e3585, 0x106aa070,
    0x19a4c116, 0x1e376c08, 0x2748774c, 0x34b0bcb5,
    0x391c0cb3, 0x4ed8aa4a, 0x5b9cca4f, 0x682e6ff3,
    0x748f82ee, 0x78a5636f, 0x84c87814, 0x8cc70208,
    0x90befffa, 0xa4506ceb, 0xbef9a3f7, 0xc67178f2,
]

# SHA-256 Constants: Initial hash values H[0...7]
H0 = [
    0x6a09e667, 0xbb67ae85, 0x3c6ef372, 0xa54ff53a,
    0x510e527f, 0x9b05688c, 0x1f83d9ab, 0x5be0cd19,
]


# --- Helper functions to simulate C macros and bitwise operations ---

def rotl32(x, n):
    """Performs a 32-bit rotate left, equivalent to ROTL32 macro."""
    return ((x << n) & 0xFFFFFFFF) | (x >> (32 - n))


def choice(x, y, z):
    """Equivalent to Choice(x,y,z) macro."""
    return (z ^ (x & (y ^ z)))


def majority(x, y, z):
    """Equivalent to Majority(x,y,z) macro."""
    return ((x & y) ^ (z & (x ^ y)))


def s0(x):
    """Equivalent to s0(x) macro."""
    return rotl32(x, 25) ^ rotl32(x, 14) ^ (x >> 3)


def s1(x):
    """Equivalent to s1(x) macro."""
    return rotl32(x, 15) ^ rotl32(x, 13) ^ (x >> 10)


def S0(x):
    """Equivalent to S0(x) macro."""
    return rotl32(x, 30) ^ rotl32(x, 19) ^ rotl32(x, 10)


def S1(x):
    """Equivalent to S1(x) macro."""
    return rotl32(x, 26) ^ rotl32(x, 21) ^ rotl32(x, 7)


# --- Core SHA-256 Implementation ---

class Sha256Ctx:
    """A class that holds the SHA-256 context, equivalent to sha256_ctx struct."""

    def __init__(self):
        self.state = [0] * _SHA256_DIGEST_LENGTH
        self.block = bytearray(SHA256_BLOCK_SIZE)
        self.index = 0
        self.total_length = 0  # CORRECTION: Added to track total message length

    def init(self):
        """Initializes the context with standard values."""
        self.state = list(H0)
        self.index = 0
        self.total_length = 0  # CORRECTION: Reset total length

    def _compress(self, block_data):
        """
        The core compression function. Corresponds to _nettle_sha256_compress.
        Processes one 64-byte block of data.
        """
        w = [0] * 16
        for i in range(16):
            offset = i * 4
            w[i] = int.from_bytes(block_data[offset:offset + 4], 'big')

        a, b, c, d, e, f, g, h = self.state

        for i in range(64):
            if i >= 16:
                # EXPAND macro logic
                w[i & 15] = (s1(w[(i - 2) & 15]) + w[(i - 7) & 15] + s0(w[(i - 15) & 15]) + w[i & 15]) & 0xFFFFFFFF

            # ROUND macro logic
            t1 = (h + S1(e) + choice(e, f, g) + K[i] + w[i & 15]) & 0xFFFFFFFF
            t2 = (S0(a) + majority(a, b, c)) & 0xFFFFFFFF

            h = g
            g = f
            f = e
            e = (d + t1) & 0xFFFFFFFF
            d = c
            c = b
            b = a
            a = (t1 + t2) & 0xFFFFFFFF

        self.state[0] = (self.state[0] + a) & 0xFFFFFFFF
        self.state[1] = (self.state[1] + b) & 0xFFFFFFFF
        self.state[2] = (self.state[2] + c) & 0xFFFFFFFF
        self.state[3] = (self.state[3] + d) & 0xFFFFFFFF
        self.state[4] = (self.state[4] + e) & 0xFFFFFFFF
        self.state[5] = (self.state[5] + f) & 0xFFFFFFFF
        self.state[6] = (self.state[6] + g) & 0xFFFFFFFF
        self.state[7] = (self.state[7] + h) & 0xFFFFFFFF

    def update(self, data):
        """
        Processes input data, buffering and calling _compress as needed.
        Corresponds to sha256_update and the MD_UPDATE macro logic.
        """
        data_len = len(data)
        self.total_length += data_len  # CORRECTION: Update total length
        data_pos = 0

        if self.index > 0:
            left = SHA256_BLOCK_SIZE - self.index
            if data_len < left:
                self.block[self.index:self.index + data_len] = data
                self.index += data_len
                return  # Finished
            else:
                self.block[self.index:] = data[:left]
                self._compress(self.block)
                data_pos += left

        while data_pos + SHA256_BLOCK_SIZE <= data_len:
            self._compress(data[data_pos:data_pos + SHA256_BLOCK_SIZE])
            data_pos += SHA256_BLOCK_SIZE

        remaining = data_len - data_pos
        self.block[:remaining] = data[data_pos:]
        self.index = remaining

    def digest(self):
        """
        Finalizes the hash, handling padding and returning the digest.
        Corresponds to sha256_digest and MD_PAD macro logic.
        """
        # Padding: Add the 0x80 byte
        self.block[self.index] = 0x80
        self.index += 1

        # If not enough space for the 8-byte length, pad and compress
        if self.index > SHA256_BLOCK_SIZE - 8:
            self.block[self.index:] = b'\x00' * (SHA256_BLOCK_SIZE - self.index)
            self._compress(self.block)
            self.index = 0

        # Pad with zeros until the length area
        self.block[self.index:SHA256_BLOCK_SIZE - 8] = b'\x00' * (SHA256_BLOCK_SIZE - 8 - self.index)

        # Append original message length in bits (big-endian)
        # CORRECTION: Use the tracked total_length for an accurate bit count.
        bit_count = self.total_length * 8
        self.block[SHA256_BLOCK_SIZE - 8:] = bit_count.to_bytes(8, 'big')
        self._compress(self.block)

        # Convert final state to big-endian byte digest
        digest_bytes = bytearray()
        for s in self.state:
            digest_bytes.extend(s.to_bytes(4, 'big'))

        # Reset context for any future use
        self.init()
        return digest_bytes


# --- Benchmark Setup and Execution ---

# The message to be hashed, as a bytes object
msg = b"abcdbcdecdefdefgefghfghighijhijkijkljklmklmnlmnomnopnopq"

# The expected correct hash result
expected_hash = bytes([
    0x24, 0x8d, 0x6a, 0x61, 0xd2, 0x06, 0x38, 0xb8, 0xe5, 0xc0, 0x26, 0x93,
    0x0c, 0x3e, 0x60, 0x39, 0xa3, 0x3c, 0xe4, 0x59, 0x64, 0xff, 0x21, 0x67,
    0xf6, 0xec, 0xed, 0xd4, 0x19, 0xdb, 0x06, 0xc1
])

# Global buffer to store the result, for verification
buffer = bytearray(SHA256_DIGEST_SIZE)


def benchmark_body(rpt):
    """The main benchmark loop."""
    global buffer
    ctx = Sha256Ctx()
    for _ in range(rpt):
        ctx.init()
        ctx.update(msg)
        buffer = ctx.digest()
    return 0


def verify_benchmark(res):
    """Verifies that the generated hash matches the expected hash."""
    is_ok = (buffer == expected_hash)
    print(f"Verification - Hash match: {'OK' if is_ok else 'FAIL'}")
    return is_ok


def main():
    """Main entry point."""
    rpt = LOCAL_SCALE_FACTOR * CPU_MHZ
    result = benchmark_body(rpt)

    print(f"Final result code: {result}")
    verify_benchmark(result)


if __name__ == "__main__":
    main()