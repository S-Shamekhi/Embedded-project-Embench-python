# This scale factor will be changed to equalize the runtime of the benchmarks.
CPU_MHZ = 100
LOCAL_SCALE_FACTOR = 1478

# Global variables to mirror the C code's structure.
# They are sized to 20x20 as in the C code.
A = [[0] * 20 for _ in range(20)]
B = [0] * 20
X = [0] * 20


def ludcmp(nmax, n):
    """
    Performs LU decomposition to solve the linear equation system Ax = B.
    This function modifies the global matrices A and X.
    """
    global A, B, X

    # Local array for intermediate results, similar to 'y[100]' in C.
    y = [0] * 100

    # --- LU Decomposition Phase ---
    # This phase modifies the matrix A in-place to store L and U matrices.
    for i in range(n):
        # Part 1: Calculate the lower triangular matrix elements
        for j in range(i + 1, n + 1):
            w = A[j][i]
            if i != 0:
                for k in range(i):
                    w -= A[j][k] * A[k][i]
            # NOTE: In C, division of integers results in an integer.
            # In Python, we must use the '//' operator for integer division.
            A[j][i] = w // A[i][i]

        # Part 2: Calculate the upper triangular matrix elements
        for j in range(i + 1, n + 1):
            w = A[i + 1][j]
            for k in range(i + 1):
                w -= A[i + 1][k] * A[k][j]
            A[i + 1][j] = w

    # --- Forward Substitution ---
    # Solves the system Ly = B for y.
    y[0] = B[0]
    for i in range(1, n + 1):
        w = B[i]
        for j in range(i):
            w -= A[i][j] * y[j]
        y[i] = w

    # --- Backward Substitution ---
    # Solves the system Ux = y for X.
    X[n] = y[n] // A[n][n]
    for i in range(n - 1, -1, -1):  # Corresponds to for(i = n-1; i >= 0; i--)
        w = y[i]
        for j in range(i + 1, n + 1):
            w -= A[i][j] * X[j]
        X[i] = w // A[i][i]

    return 0


def benchmark_body(rpt):
    """
    The main body of the benchmark. It initializes a matrix and vector,
    then calls the LU decomposition solver.
    """
    # The C code writes to a volatile variable 'chkerr'. We'll just use a
    # normal variable to hold the return value.
    err_code = 0

    for _ in range(rpt):
        nmax = 20
        n = 5

        # Initialize the matrix 'A' and vector 'B'.
        # This is done inside the loop to reset the data for each run.
        for i in range(n + 1):
            w = 0
            for j in range(n + 1):
                val = (i + 1) + (j + 1)
                if i == j:
                    val *= 2
                A[i][j] = val
                w += A[i][j]
            B[i] = w

        err_code = ludcmp(nmax, n)

    return err_code


def verify_benchmark(res):
    """
    Verifies that the result vector X matches the expected reference values.
    """
    x_ref = [0, 0, 1, 1, 1, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]

    # In Python, we can compare the slices of the lists directly.
    is_x_ok = (X == x_ref)
    is_res_ok = (res == 0)

    print(f"Verification - Result vector X: {'OK' if is_x_ok else 'FAIL'}")
    print(f"Verification - Return code: {'OK' if is_res_ok else 'FAIL'}")

    return is_x_ok and is_res_ok


def main():
    """The main entry point of the program."""
    rpt = LOCAL_SCALE_FACTOR * CPU_MHZ
    result = benchmark_body(rpt)

    print(f"Final return code: {result}")

    verify_benchmark(result)


if __name__ == "__main__":
    main()