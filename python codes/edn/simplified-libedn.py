# Simplified libedn
N = 10
ORDER = 3

# Example arrays
a = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
b = [2, -1, 3, -2, 1, 0, -1, 2, -3, 1]
output = [0] * N

def vec_mpy_simple(y, x, scaler):
    for i in range(len(y)):
        y[i] += scaler * x[i]

def dot_product(a_list, b_list):
    result = 0
    for i in range(len(a_list)):
        result += a_list[i] * b_list[i]
    return result

def fir_simple(array, coeff):
    out = []
    for i in range(len(array) - len(coeff) + 1):
        s = 0
        for j in range(len(coeff)):
            s += array[i + j] * coeff[j]
        out.append(s)
    return out

# Run simplified example
vec_mpy_simple(a, b, 2)
dp = dot_product(a, b)
output = fir_simple(a, [1, -1, 2])

print("Vector multiply result:", a)
print("Dot product result:", dp)
print("FIR filter result:", output)
