# BEEBS nbody benchmark - Python conversion
# Based on the original C version (GPL-3.0-or-later, BSD portions)
import math

# Constants
PI = 3.141592653589793
SOLAR_MASS = 4 * PI * PI
DAYS_PER_YEAR = 365.24

class Body:
    def __init__(self, x, v, mass):
        self.x = x[:]  # position vector
        self.v = v[:]  # velocity vector
        self.mass = mass

# Solar system bodies (Sun + 4 giant planets)
solar_bodies = [
    Body([0.0, 0.0, 0.0],
         [0.0, 0.0, 0.0],
         SOLAR_MASS),
    Body([4.84143144246472090e+00,
          -1.16032004402742839e+00,
          -1.03622044471123109e-01],
         [1.66007664274403694e-03 * DAYS_PER_YEAR,
          7.69901118419740425e-03 * DAYS_PER_YEAR,
          -6.90460016972063023e-05 * DAYS_PER_YEAR],
         9.54791938424326609e-04 * SOLAR_MASS),
    Body([8.34336671824457987e+00,
          4.12479856412430479e+00,
          -4.03523417114321381e-01],
         [-2.76742510726862411e-03 * DAYS_PER_YEAR,
          4.99852801234917238e-03 * DAYS_PER_YEAR,
          2.30417297573763929e-05 * DAYS_PER_YEAR],
         2.85885980666130812e-04 * SOLAR_MASS),
    Body([1.28943695621391310e+01,
          -1.51111514016986312e+01,
          -2.23307578892655734e-01],
         [2.96460137564761618e-03 * DAYS_PER_YEAR,
          2.37847173959480950e-03 * DAYS_PER_YEAR,
          -2.96589568540237556e-05 * DAYS_PER_YEAR],
         4.36624404335156298e-05 * SOLAR_MASS),
    Body([1.53796971148509165e+01,
          -2.59193146099879641e+01,
          1.79258772950371181e-01],
         [2.68067772490389322e-03 * DAYS_PER_YEAR,
          1.62824170038242295e-03 * DAYS_PER_YEAR,
          -9.51592254519715870e-05 * DAYS_PER_YEAR],
         5.15138902046611451e-05 * SOLAR_MASS),
]

def offset_momentum(bodies):
    """Adjust momentum so that total momentum = 0 (stabilises the system)."""
    px = py = pz = 0.0
    for b in bodies:
        px += b.v[0] * b.mass
        py += b.v[1] * b.mass
        pz += b.v[2] * b.mass
    bodies[0].v[0] -= px / SOLAR_MASS
    bodies[0].v[1] -= py / SOLAR_MASS
    bodies[0].v[2] -= pz / SOLAR_MASS

def bodies_energy(bodies):
    """Compute the total energy (kinetic + potential) of the system."""
    e = 0.0
    for i in range(len(bodies)):
        b = bodies[i]
        # kinetic energy
        e += b.mass * (b.v[0]**2 + b.v[1]**2 + b.v[2]**2) / 2.0
        # potential energy with other bodies
        for j in range(i+1, len(bodies)):
            dx = b.x[0] - bodies[j].x[0]
            dy = b.x[1] - bodies[j].x[1]
            dz = b.x[2] - bodies[j].x[2]
            distance = math.sqrt(dx*dx + dy*dy + dz*dz)
            e -= (b.mass * bodies[j].mass) / distance
    return e

def benchmark_body(rpt=1):
    """Main benchmark loop."""
    tot_e = 0.0
    for _ in range(rpt):
        offset_momentum(solar_bodies)
        tot_e = 0.0
        for _ in range(100):
            tot_e += bodies_energy(solar_bodies)
    # Known good value for correctness
    expected = -16.907516382852478
    return abs(tot_e - expected) < 1e-9

if __name__ == "__main__":
    ok = benchmark_body(1)
    print("Verification:", "PASS" if ok else "FAIL")
