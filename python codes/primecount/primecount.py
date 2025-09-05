# primecount.py

# Constants (matching the C definitions)
LOCAL_SCALE_FACTOR = 1
SZ = 42               # Size of sieve/primes arrays
NPRIMES = 3512        # Expected number of primes

def count_primes():
    """
    Counts the number of prime numbers using a custom sieve method.
    """
    primes = [0] * SZ   # Array to store primes
    sieve = [0] * SZ    # Array to store sieve multiples

    n_sieve = 0
    primes[0] = 2
    sieve[0] = 4
    n_sieve += 1

    n_primes = 1
    trial = 3
    sqr = 2

    while True:
        while sqr * sqr <= trial:
            sqr += 1
        sqr -= 1

        for i in range(n_sieve):
            if primes[i] > sqr:
                # Found a prime
                if n_sieve < SZ:
                    primes[n_sieve] = trial
                    sieve[n_sieve] = trial * trial
                    n_sieve += 1
                n_primes += 1
                trial += 1
                break
            while sieve[i] < trial:
                sieve[i] += primes[i]
            if sieve[i] == trial:
                trial += 1
                break
        else:
            # No divisors found → exit
            break

    return n_primes


def benchmark_body(rpt):
    """
    Repeats the prime counting benchmark 'rpt' times.
    """
    r = 0
    for _ in range(rpt):
        r = count_primes()
    return r


def warm_caches(heat):
    """
    Simulates warming up caches by running the benchmark.
    """
    _ = benchmark_body(heat)


def benchmark(cpu_mhz=1):
    """
    Runs the benchmark, scaling iterations by CPU speed.
    """
    return benchmark_body(LOCAL_SCALE_FACTOR * cpu_mhz)


def initialise_benchmark():
    """
    Placeholder for initialization (no-op in this case).
    """
    pass


def verify_benchmark(result):
    """
    Verifies that the benchmark result matches the expected number of primes.
    """
    return result == NPRIMES


if __name__ == "__main__":
    # Example execution
    result = benchmark(1)  # CPU_MHZ assumed = 1 for Python
    print("Primes counted:", result)
    print("Verification:", "PASS" if verify_benchmark(result) else "FAIL")
