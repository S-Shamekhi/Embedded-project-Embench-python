

### **Overview**

This program benchmarks the performance of **matrix multiplication**. It generates two random 20×20 matrices, multiplies them, and stores the result in a third matrix.
It is used to test how efficiently a compiler or embedded system handles nested loops, multidimensional arrays, and arithmetic operations.

---

### **Key Parts of the Code**

1. **Constants & Types**

   * `UPPERLIMIT = 20` → matrix size is 20×20.
   * `MOD_SIZE = 8095` → used in pseudo-random number generator.
   * `matrix` → in C, this is just a `long int [20][20]`. In Python we use lists of lists.

---

2. **Random Number Generator**

   * The code uses its own generator, `RandomInteger()`, instead of `rand()`.
   * Formula:

     ```
     Seed = ((Seed * 133) + 81) % 8095
     ```
   * Ensures the same “random” sequence every run → reproducibility.

---

3. **Matrix Multiplication (`Multiply`)**

   * Classic triple-loop:

     * Outer loop: iterate over rows of `A`.
     * Inner loop: iterate over columns of `B`.
     * Index loop: sum products of row elements from `A` and column elements from `B`.
   * Stores result in `Res[Outer][Inner]`.

---

4. **Benchmark Function**

   * `benchmark_body(rpt)` runs the multiplication test `rpt` times.
   * `benchmark()` scales this by a factor depending on CPU speed.
   * Purpose: simulate workload to measure execution time.

---

5. **Initialization**

   * `initialise_benchmark()` fills `ArrayA_ref` and `ArrayB_ref` with random values using `RandomInteger()`.
   * Before each multiplication, these reference arrays are copied into working arrays `ArrayA` and `ArrayB`.

---

6. **Verification**

   * In C, `verify_benchmark()` compares the result with a large precomputed expected matrix (`exp`).
   * In Python, we can keep just one row (or compute a checksum) to validate correctness without storing all 400 numbers.

---

### **In short**

* The code **generates two 20×20 random matrices**.
* **Multiplies them together** using a nested loop.
* Runs the multiplication multiple times for benchmarking.
* **Verifies correctness** by comparing the result with a known good output.

---
### **Output**
<img width="439" height="67" alt="image" src="https://github.com/user-attachments/assets/5faeec6b-8040-4867-8126-f5145a31066b" />
