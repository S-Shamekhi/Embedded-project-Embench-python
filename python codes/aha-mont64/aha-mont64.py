#
# This file is a pure Python implementation of the aha-mont64 benchmark.
# It focuses on 64-bit and 128-bit integer arithmetic, particularly
# for Montgomery Multiplication.
# THIS IS THE CORRECTED VERSION.
#

# --- Constants and Initial Values ---
CPU_MHZ = 100
LOCAL_SCALE_FACTOR = 423

# Mask to simulate 64-bit unsigned integers
MASK64 = 0xFFFFFFFFFFFFFFFF

# Initial values for the benchmark, taken from initialise_benchmark()
IN_M = 0xfae849273928f89f  # Must be odd
IN_B = 0x14736defb9330573  # Must be smaller than m
IN_A = 0x0549372187237fef  # Must be smaller than m


def mulul64(u, v):
    """
    Multiplies two 64-bit unsigned integers to produce a 128-bit result.
    In Python, this is trivial due to arbitrary-precision integers.
    Returns (high_64_bits, low_64_bits).
    """
    result = u * v
    wlo = result & MASK64
    whi = result >> 64
    return whi, wlo


def modul64(x, y, z):
    """
    Divides a 128-bit integer (x || y) by a 64-bit integer z,
    returning the remainder.
    Python's integers make this a single operation.
    """
    dividend = (x << 64) | y
    return dividend % z


def xbinGCD(a, b):
    """
    Implements the extended binary GCD algorithm, simplified for the case
    where 'a' is a power of 2 and 'b' is odd.
    Returns (u, v) such that gcd(2*a,b) = u*(2*a) - v*b.
    """
    u = 1
    v = 0
    alpha = a
    beta = b

    while a > 0:
        a = a >> 1
        if (u & 1) == 0:  # If u is even
            u = u >> 1
            v = v >> 1
        else:
            # (u + beta) / 2
            u = (u + beta) // 2
            # CORRECTION IS HERE: This line was previously incorrect.
            # It should be (v/2) + alpha.
            v = (v // 2) + alpha
    return u, v


def montmul(abar, bbar, m, mprime):
    """
    Computes a*b mod m using Montgomery Multiplication.
    """
    # t = abar * bbar (128-bit result)
    thi, tlo = mulul64(abar, bbar)

    # tm = (t * mprime) & MASK64
    tm = (tlo * mprime) & MASK64

    # tmm = tm * m (128-bit result)
    tmmhi, tmmlo = mulul64(tm, m)

    # u = t + tmm (128-bit addition)
    # Python's integers handle the 128-bit addition and carries automatically.
    u = ((thi << 64) | tlo) + ((tmmhi << 64) | tmmlo)

    # Shift u right 64 bits to get the result
    ulo = u >> 64

    # The C code checks for overflow from the 128-bit addition.
    # We can check if the 129th bit (or higher) is set.
    overflow = u >> 128 > 0

    # If u >= m, subtract m from u.
    # The C code uses a branchless trick; a simple if is clearer in Python.
    if overflow or ulo >= m:
        ulo = ulo - m

    return ulo


def benchmark_body(rpt):
    """The main benchmark loop."""
    errors = 0
    for _ in range(rpt):
        m = IN_M
        b = IN_B
        a = IN_A

        # --- Method 1: Simple Calculation ---
        # Computes (a*b)**4 mod m using direct 128-bit arithmetic.
        # p1 = (a * b) % m
        p1hi, p1lo = mulul64(a, b)
        p1 = modul64(p1hi, p1lo, m)
        # p1 = (p1 * p1) % m
        p1hi, p1lo = mulul64(p1, p1)
        p1 = modul64(p1hi, p1lo, m)
        # p1 = (p1 * p1) % m
        p1hi, p1lo = mulul64(p1, p1)
        p1 = modul64(p1hi, p1lo, m)

        # --- Method 2: Montgomery Multiplication ---
        # r is fixed at 2**64. hr is half of r.
        hr = 0x8000000000000000

        # Find rinv and mprime such that r*rinv - m*mprime = 1
        rinv, mprime = xbinGCD(hr, m)

        # Convert a and b to Montgomery domain: (n * r) % m
        # (a << 64) % m
        abar = modul64(a, 0, m)
        bbar = modul64(b, 0, m)

        # Perform multiplications in Montgomery domain
        p = montmul(abar, bbar, m, mprime)
        p = montmul(p, p, m, mprime)
        p = montmul(p, p, m, mprime)

        # Convert result back from Montgomery domain: (p * r_inverse) % m
        phi, plo = mulul64(p, rinv)
        p = modul64(phi, plo, m)

        if p != p1:
            errors = 1

    return errors


def verify_benchmark(r):
    """Verification: r is the number of errors, so it should be 0."""
    return r == 0


def main():
    """Main entry point."""
    rpt = LOCAL_SCALE_FACTOR * CPU_MHZ
    result = benchmark_body(rpt)

    print(f"Final error count: {result}")

    if verify_benchmark(result):
        print("Verification: OK")
    else:
        print("Verification: FAIL")


if __name__ == "__main__":
    main()