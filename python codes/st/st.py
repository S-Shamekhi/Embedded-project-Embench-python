import math

# This scale factor will be changed to equalize the runtime of the benchmarks.
# The CPU_MHZ and LOCAL_SCALE_FACTOR values are taken from the C code.
CPU_MHZ = 100
LOCAL_SCALE_FACTOR = 13

# Constants
MAX = 100

# Global variables to simulate the C code's structure.
SEED = 0
ARRAY_A = [0.0] * MAX
ARRAY_B = [0.0] * MAX
SUM_A = 0.0
SUM_B = 0.0
COEF = 0.0


def init_seed():
    """Initializes the seed for the random number generator."""
    global SEED
    SEED = 0


def random_integer():
    """
    Generates a random integer between 0 and 8095 using a linear congruential generator.
    """
    global SEED
    SEED = ((SEED * 133) + 81) % 8095
    return SEED


def initialize(array):
    """
    Initializes the given array with random numbers.
    """
    for i in range(MAX):
        array[i] = i + random_integer() / 8095.0


def square(x):
    """Returns the square of a number."""
    return x * x


def calc_sum_mean(array):
    """
    Calculates and returns the sum and mean of the elements in an array.
    In Python, we return a tuple instead of using pointers.
    """
    sum_val = 0.0
    for i in range(MAX):
        sum_val += array[i]
    mean_val = sum_val / MAX
    return sum_val, mean_val


def calc_var_stddev(array, mean):
    """
    Calculates the variance and standard deviation of an array.
    """
    diffs = 0.0
    for i in range(MAX):
        diffs += square(array[i] - mean)
    var_val = diffs / MAX
    stddev_val = math.sqrt(var_val)
    return var_val, stddev_val


def calc_lin_corr_coef(array_a, array_b, mean_a, mean_b):
    """
    Calculates the linear (Pearson) correlation coefficient between two arrays.
    The result is stored in the global variable COEF to mimic the C code's behavior.
    """
    global COEF
    numerator = 0.0
    aterm = 0.0
    bterm = 0.0
    for i in range(MAX):
        numerator += (array_a[i] - mean_a) * (array_b[i] - mean_b)
        aterm += square(array_a[i] - mean_a)
        bterm += square(array_b[i] - mean_b)

    COEF = numerator / (math.sqrt(aterm) * math.sqrt(bterm))


def benchmark_body(rpt):
    """
    The main body of the benchmark, which repeats the statistical calculations 'rpt' times.
    """
    global SUM_A, SUM_B  # Needed to assign to these global variables

    for _ in range(rpt):
        init_seed()

        initialize(ARRAY_A)
        SUM_A, mean_a = calc_sum_mean(ARRAY_A)
        _, _ = calc_var_stddev(ARRAY_A, mean_a)  # The return values are not used

        initialize(ARRAY_B)
        SUM_B, mean_b = calc_sum_mean(ARRAY_B)
        _, _ = calc_var_stddev(ARRAY_B, mean_b)

        calc_lin_corr_coef(ARRAY_A, ARRAY_B, mean_a, mean_b)


def verify_benchmark():
    """
    Compares the final results with expected values to ensure correctness.
    """
    exp_sum_a = 4999.00247066090196
    exp_sum_b = 4996.84311303273534
    exp_coef = 0.999900054853619324

    # For comparing floating-point numbers, we use math.isclose()
    sum_a_ok = math.isclose(exp_sum_a, SUM_A)
    sum_b_ok = math.isclose(exp_sum_b, SUM_B)
    coef_ok = math.isclose(exp_coef, COEF)

    print(f"Verification - SumA: {'OK' if sum_a_ok else 'FAIL'}")
    print(f"Verification - SumB: {'OK' if sum_b_ok else 'FAIL'}")
    print(f"Verification - Coef: {'OK' if coef_ok else 'FAIL'}")

    return sum_a_ok and sum_b_ok and coef_ok


def main():
    """The main entry point of the program."""
    # Run the main benchmark body
    # The repetition count (rpt) is calculated similarly to the C code.
    rpt = LOCAL_SCALE_FACTOR * CPU_MHZ
    benchmark_body(rpt)

    # Print final results for inspection
    print(f"Final SumA: {SUM_A}")
    print(f"Final SumB: {SUM_B}")
    print(f"Final Coef: {COEF}")

    # Verify the results
    verify_benchmark()


if __name__ == "__main__":
    main()