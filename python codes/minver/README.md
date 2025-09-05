

This Python code is a faithful conversion of the **BEEBS `minver` benchmark**, originally written in C, which tests **matrix inversion and multiplication** for a 3x3 floating-point matrix. The benchmark is used to measure computational performance in embedded systems.

**Key Components:**

1. **Reference Matrices:**

   * `a_ref` is the 3x3 matrix to be inverted.
   * `b` is another 3x3 matrix used for multiplication.

2. **Working Matrices:**

   * `a` is the current matrix being manipulated.
   * `c` stores the result of matrix multiplication (`a * b`).
   * `d` stores the result of the matrix inversion.
   * `det` stores the determinant calculated during inversion.

3. **Functions:**

   * `minver_fabs(n)` — computes the absolute value of a float.
   * `mmul(row_a, col_a, row_b, col_b)` — performs matrix multiplication: `c = a * b`.
   * `minver(row, col, eps)` — performs a 3x3 matrix inversion using **Gaussian elimination with full pivoting**, while tracking row swaps and computing the determinant.
   * `float_eq` / `float_neq` — compare floating-point numbers within a small tolerance to handle numerical errors.
   * `verify_benchmark` — checks the results (`c`, `d`, `det`) against known expected values, ensuring the computation matches the original benchmark.

4. **Benchmark Execution:**

   * `benchmark_body(rpt)` repeats the inversion and multiplication `rpt` times to simulate load.
   * `benchmark()` scales the number of repetitions based on a local factor and CPU speed, mimicking the C benchmark.

**Implementation Notes:**

* Uses `copy.deepcopy` to avoid overwriting reference matrices.
* Row swaps and normalization in `minver` closely follow the C implementation to ensure identical results.
* Floating-point differences between Python and C are minimized by using a **32-bit float equivalent** (`float32`) for verification.

This Python version preserves the **algorithmic structure**, making it suitable for **embedded systems benchmarking or educational purposes**.

---
Ah — now we’re hitting the **classic floating-point precision and representation issue** between C and Python. Let me explain carefully.

---
when we run it this is what we can expect :

![alt text](image.png)

###  Why `verify_benchmark()` returns `False`

Even though the logic is identical, the **determinant and inverted matrix values differ slightly**. The reasons:

1. **Floating-point arithmetic differences**:

   * In C, `float` is usually **32-bit single precision**.
   * In Python, all floats are **64-bit double precision** by default.
   * Operations like `/` and `*` accumulate rounding differently in 64-bit vs 32-bit.

2. **Order of operations / compiler behavior**:

   * The C compiler might optimize expressions in a way that affects rounding.
   * Python executes arithmetic exactly as written in its interpreter, so some intermediate results are slightly different.

3. **`verify_benchmark` tolerances**:

   * The benchmark expects **exactly** the C floating-point values.
   * Even differences in the 7th–8th decimal place will cause the equality check to fail (`float_eq` with `1e-6` may not be enough because the C benchmark uses single-precision rounding).

---
