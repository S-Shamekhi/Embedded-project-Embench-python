# libEDN Python Conversion
this folder has 2 python files , here is what does each include : 
## Original
- Full Python translation of EDN benchmark from Embench.
- Simulates digital signal processing (DSP) tasks: vector multiply, dot product, FIR/IIR filtering, lattice synthesis, JPEG DCT, vocoder codebook search.
- Designed to stress CPU and memory like real embedded systems.
- Verification may fail in Python due to integer overflow differences from C.

## Simplified
- Focuses on core DSP concepts: vector multiply, dot product, FIR filter.
- Easy to understand and use for learning signal processing basics.
- Shows how input signals are transformed via simple arithmetic operations.
- Expected outputs are predictable and illustrate key DSP concepts.



### **A. Introduction to Embench / EDN**

* **Embench** is a suite of **embedded benchmarks** for evaluating CPU and compiler performance.
* **EDN (Embedded Digital Numerics)** benchmark simulates **digital signal processing (DSP)** tasks like:

  * Audio processing (filters, vocoders)
  * Image processing (JPEG DCT)
  * Vector arithmetic and linear algebra
* Purpose: measure **execution efficiency, memory access patterns, and compiler optimization impact**.

---

### **B. Key functions in the original EDN benchmark**

| Function                | What it does                                                   | Real-world use                             |
| ----------------------- | -------------------------------------------------------------- | ------------------------------------------ |
| `vec_mpy1`              | Multiplies two vectors element-wise and accumulates the result | Signal mixing, scaling audio samples       |
| `mac`                   | Computes dot product and sum of squares                        | Correlation, energy measurement in signals |
| `fir` / `fir_no_red_ld` | FIR (Finite Impulse Response) filter                           | Audio/electrical signal filtering          |
| `latsynth`              | Lattice synthesis (speech signal generation)                   | Vocoder / speech synthesis                 |
| `iir1`                  | IIR (Infinite Impulse Response) filter                         | Feedback-based audio filtering             |
| `codebook`              | Chooses best matching vector from a codebook                   | Speech compression / encoding              |
| `jpegdct`               | JPEG Discrete Cosine Transform                                 | Image compression                          |

> Notes:
>
> * These functions stress **CPU computation** and **memory handling**, common in embedded DSP systems.
> * Original C code relies on **16-bit / 32-bit integer arithmetic** and **bit shifts**, which behave differently in Python.

---

### **C. Original Python Conversion**

* Converted to Python while keeping **all operations**.
* Verification: `False` because Python **doesn’t automatically overflow integers** like C does.
  what does this mean?
  if we run the python file we will get this result  :
  
  <img width="480" height="54" alt="image" src="https://github.com/user-attachments/assets/aa7f058d-c178-4697-943f-c062c0e7dce9" />

* Useful for:

  * Understanding **algorithm logic**
  * Checking **function-level correctness**
* Limitation: For exact numeric verification, need to **emulate 16-bit / 32-bit overflow**.
  **the difference in how C and Python handle integers , which directly affects the benchmark verification.**

---

### **1️⃣ Conversion to Python**

* The original EDN code is written in **C**, which uses fixed-size integers:

  * `short` → typically 16 bits (range: -32,768 to 32,767)
  * `long int` → typically 32 bits
* In C, arithmetic **wraps around automatically** if a calculation exceeds the type’s limit.

  * Example: `32767 + 1` → `-32768` (overflow)
* The Python version keeps the **same arithmetic operations**, loops, and logic but uses **Python integers**, which are **arbitrary-precision** (they never overflow naturally).

  * Example: `32767 + 1` → `32768` (no wraparound)

---

### **2️⃣ Why Verification Fails**

* The EDN benchmark has a **verification step**: it compares the computed output to **expected C results**, including the effects of **overflow**.
* Since Python integers don’t overflow, the values differ, causing:

```python
Verification: False
```

* This is **normal** and doesn’t mean the logic is wrong—it’s just a **C vs Python integer behavior mismatch**.

---

### **3️⃣ Why it’s still useful**

Even if the numeric verification fails:

1. **Algorithm logic**:

   * You can see **how vectors, filters, and other operations work**.
   * Understand loops, accumulations, and arithmetic structure.
2. **Function-level correctness**:

   * You can test individual functions (like `vec_mpy1` or `fir`) to see the **sequence of operations**, independent of integer wraparound.

---

### **4️⃣ How to emulate C behavior if needed**

* If you want **exact numeric verification**, you need to **simulate 16-bit / 32-bit integers** in Python:

```python
def int16(x):
    x = x & 0xFFFF  # mask to 16 bits
    if x >= 0x8000:  # if negative in C
        x -= 0x10000
    return x

def int32(x):
    x = x & 0xFFFFFFFF
    if x >= 0x80000000:
        x -= 0x100000000
    return x
```

* Then apply `int16()` or `int32()` after every arithmetic operation.
* This will make Python **match C’s results exactly**, and verification would pass.


---

### **D. Simplified version**

* Removes **complex DSP operations** (IIR, lattice synthesis, JPEG DCT, codebook search).
* Focuses on:

  1. **Vector multiply**
  2. **Dot product**
  3. **FIR filter**
* Purpose:

  * Help learners understand the **core DSP concepts** without overwhelming detail.
  * Demonstrates **how input signals are transformed by simple arithmetic operations**.
* Expected output: shows scaled vectors, single number dot product, and filtered sequences.
* Connects to real DSP use:

  * Vector multiply = mixing signals
  * Dot product = correlation / energy
  * FIR = smoothing / filtering a signal

---
