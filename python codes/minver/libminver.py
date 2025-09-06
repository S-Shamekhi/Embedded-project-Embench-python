import copy

# Reference matrices
a_ref = [
    [3.0, -6.0, 7.0],
    [9.0, 0.0, -5.0],
    [5.0, -8.0, 6.0]
]

b = [
    [-3.0, 0.0, 2.0],
    [3.0, -2.0, 0.0],
    [0.0, 2.0, -3.0]
]

# Working matrices
a = [[0.0]*3 for _ in range(3)]
c = [[0.0]*3 for _ in range(3)]
d = [[0.0]*3 for _ in range(3)]
det = 0.0

# Absolute value function
def minver_fabs(n):
    return n if n >= 0 else -n

# Matrix multiplication (a * b -> c)
def mmul(row_a, col_a, row_b, col_b):
    global c
    if row_a < 1 or row_b < 1 or col_a != row_b:
        return 999
    for i in range(row_a):
        for j in range(col_b):
            w = 0.0
            for k in range(row_b):
                w += a[i][k] * b[k][j]
            c[i][j] = w
    return 0

# Matrix inversion for 3x3 with full fidelity
def minver(row, col, eps):
    global a, det
    work = list(range(500))
    w1 = 1.0

    if row < 2 or row > 500 or eps <= 0.0:
        return 999

    for i in range(row):
        work[i] = i

    for k in range(row):
        # Find pivot
        wmax = 0.0
        r = k
        for i in range(k, row):
            w = minver_fabs(a[i][k])
            if w > wmax:
                wmax = w
                r = i

        pivot = a[r][k]
        api = minver_fabs(pivot)
        if api <= eps:
            det = w1
            return 1
        w1 *= pivot

        # Row swaps
        if r != k:
            work[k], work[r] = work[r], work[k]
            a[k], a[r] = a[r], a[k]
            w1 = -w1

        # Normalize pivot row
        for i in range(row):
            a[k][i] /= pivot

        # Eliminate other rows
        for i in range(row):
            if i != k:
                w = a[i][k]
                if w != 0.0:
                    for j in range(row):
                        if j != k:
                            a[i][j] -= w * a[k][j]
                    a[i][k] = -w / pivot

        a[k][k] = 1.0 / pivot

    # Undo row swaps
    for i in range(row):
        while True:
            k = work[i]
            if k == i:
                break
            work[k], work[i] = work[i], work[k]
            for j in range(row):
                a[k][i], a[k][k] = a[k][k], a[k][i]

    det = w1
    return 0

# Floating-point comparison functions
def float_eq(a, b, tol=1e-6):
    return minver_fabs(a-b) < tol

def float_neq(a, b, tol=1e-6):
    return not float_eq(a, b, tol)

# Verify benchmark exactly like C
def verify_benchmark(res=None):
    global a, c, d, det
    c_exp = [
        [-27.0, 26.0, -15.0],
        [-27.0, -10.0, 33.0],
        [-39.0, 28.0, -8.0]
    ]

    d_exp = [
        [0.133333325, -0.199999958, 0.2666665910],
        [-0.519999862, 0.113333330, 0.5266665220],
        [0.479999840, -0.359999895, 0.0399999917]
    ]

    for i in range(3):
        for j in range(3):
            if float_neq(c[i][j], c_exp[i][j]) or float_neq(d[i][j], d_exp[i][j]):
                return False

    return float_eq(det, -16.6666718)

# Benchmark body
def benchmark_body(rpt):
    global a, d
    for _ in range(rpt):
        eps = 1.0e-6
        a = copy.deepcopy(a_ref)
        minver(3, 3, eps)
        d = copy.deepcopy(a)
        a = copy.deepcopy(a_ref)
        mmul(3, 3, 3, 3)
    return 0

# Main benchmark function
def benchmark():
    LOCAL_SCALE_FACTOR = 555
    CPU_MHZ = 1
    return benchmark_body(LOCAL_SCALE_FACTOR * CPU_MHZ)

if __name__ == "__main__":
    benchmark()
    print("Verification:", verify_benchmark())