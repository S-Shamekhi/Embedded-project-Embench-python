LOCAL_SCALE_FACTOR = 87
N = 100
ORDER = 50

# Global arrays
a = [0] * 200
b = [0] * 200
c = 0
d = 0
e = 0
output = [0] * 200


def vec_mpy1(y, x, scaler):
    for i in range(150):
        y[i] += (scaler * x[i]) >> 15


def mac(a_list, b_list, sqr, sum_ptr):
    dotp = sum_ptr
    for i in range(150):
        dotp += b_list[i] * a_list[i]
        sqr += b_list[i] * b_list[i]
    return sqr, dotp


def fir(array1, coeff, output_list):
    for i in range(N - ORDER):
        sum_val = 0
        for j in range(ORDER):
            sum_val += array1[i + j] * coeff[j]
        output_list[i] = sum_val >> 15


def fir_no_red_ld(x, h, y):
    for j in range(0, 100, 2):
        sum0 = 0
        sum1 = 0
        x0 = x[j]
        for i in range(0, 32, 2):
            x1 = x[j + i + 1]
            h0 = h[i]
            sum0 += x0 * h0
            sum1 += x1 * h0
            x0 = x[j + i + 2]
            h1 = h[i + 1]
            sum0 += x1 * h1
            sum1 += x0 * h1
        y[j] = sum0 >> 15
        y[j + 1] = sum1 >> 15


def latsynth(b_list, k_list, n, f):
    f -= b_list[n - 1] * k_list[n - 1]
    for i in range(n - 2, -1, -1):
        f -= b_list[i] * k_list[i]
        b_list[i + 1] = b_list[i] + ((k_list[i] * (f >> 16)) >> 16)
    b_list[0] = f >> 16
    return f


def iir1(coefs, input_list, optr, state):
    x = input_list[0]
    for n in range(50):
        t = x + ((coefs[2] * state[0] + coefs[3] * state[1]) >> 15)
        x = t + ((coefs[0] * state[0] + coefs[1] * state[1]) >> 15)
        state[1] = state[0]
        state[0] = t
        coefs = coefs[4:]  # move to next filter coefs
        state = state[2:]   # move to next filter states
    optr[0] = x


def codebook(mask, bitchanged, numbasis, codeword, g, d_list, ddim, theta):
    for j in range(bitchanged + 1, numbasis + 1):
        # Original loop body removed in C code, so we skip
        pass
    return g


def jpegdct(d_list, r_list):
    t = [0] * 12
    k, m, n_val, p = 1, 0, 13, 8
    index = 0
    while k <= 8:
        for i in range(8):
            for j in range(4):
                t[j] = d_list[index + k * j] + d_list[index + k * (7 - j)]
                t[7 - j] = d_list[index + k * j] - d_list[index + k * (7 - j)]
            t[8] = t[0] + t[3]
            t[9] = t[0] - t[3]
            t[10] = t[1] + t[2]
            t[11] = t[1] - t[2]
            d_list[index] = (t[8] + t[10]) >> m
            d_list[index + 4 * k] = (t[8] - t[10]) >> m
            t8 = (t[11] + t[9]) * r_list[10]
            d_list[index + 2 * k] = t8 + ((t[9] * r_list[9]) >> n_val)
            d_list[index + 6 * k] = t8 + ((t[11] * r_list[11]) >> n_val)
            t[0] = (t[4] + t[7]) * r_list[2]
            t[1] = (t[5] + t[6]) * r_list[0]
            t[2] = t[4] + t[6]
            t[3] = t[5] + t[7]
            t[8] = (t[2] + t[3]) * r_list[8]
            t[2] = t[2] * r_list[1] + t[8]
            t[3] = t[3] * r_list[3] + t[8]
            d_list[index + 7 * k] = (t[4] * r_list[4] + t[0] + t[2]) >> n_val
            d_list[index + 5 * k] = (t[5] * r_list[6] + t[1] + t[3]) >> n_val
            d_list[index + 3 * k] = (t[6] * r_list[5] + t[1] + t[2]) >> n_val
            d_list[index + 1 * k] = (t[7] * r_list[7] + t[0] + t[3]) >> n_val
            index += p
        k += 7
        m += 3
        n_val += 3
        p -= 7
        index -= 64


def initialise_benchmark():
    pass


def benchmark_body(rpt):
    global a, b, c, d, e, output

    for _ in range(rpt):
        in_a = [0x0000, 0x07ff, 0x0c00, 0x0800, 0x0200, 0xf800, 0xf300, 0x0400] * 25
        in_b = [0x0c60, 0x0c40, 0x0c20, 0x0c00, 0xf600, 0xf400, 0xf200, 0xf000] * 25
        c = 0x3
        d = 0xAAAA
        e = 0xEEEE

        for i in range(200):
            a[i] = in_a[i]
            b[i] = in_b[i]

        vec_mpy1(a, b, c)
        c, _ = mac(a, b, c, output[0])
        fir(a, b, output)
        fir_no_red_ld(a, b, output)
        d = latsynth(a, b, N, d)
        iir1(a, b, output[100:], output)
        e = codebook(d, 1, 17, e, d, a, c, 1)
        jpegdct(a, b)

    return 0


def benchmark():
    # Assuming CPU_MHZ = 1 for simplicity, can be set as needed
    CPU_MHZ = 1
    return benchmark_body(LOCAL_SCALE_FACTOR * CPU_MHZ)


def verify_benchmark():
    exp_output = [3760, 4269, 3126, 1030, 2453, -4601, 1981, -1056, 2621, 4269,
                  3058, 1030, 2378, -4601, 1902, -1056, 2548, 4269, 2988, 1030,
                  2300, -4601, 1822, -1056, 2474, 4269, 2917, 1030, 2220, -4601,
                  1738, -1056, 2398, 4269, 2844, 1030, 2140, -4601, 1655, -1056,
                  2321, 4269, 2770, 1030, 2058, -4601, 1569, -1056, 2242, 4269,
                  2152, 1030, 1683, -4601, 1627, -1056, 2030, 4269, 2080, 1030,
                  1611, -4601, 1555, -1056, 1958, 4269, 2008, 1030, 1539, -4601,
                  1483, -1056, 1886, 4269, 1935, 1030, 1466, -4601, 1410, -1056,
                  1813, 4269, 1862, 1030, 1393, -4601, 1337, -1056, 1740, 4269,
                  1789, 1030, 1320, -4601, 1264, -1056, 1667, 4269, 1716, 1030,
                  1968] + [0] * 120

    return output == exp_output and c == 10243 and d == -441886230 and e == -441886230


if __name__ == "__main__":
    initialise_benchmark()
    benchmark()
    print("Verification:", verify_benchmark())
