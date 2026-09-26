# -*- coding: utf-8 -*-
"""Wall-time scaling of the FiPy cold-plate solve with mesh size (fixed sweep count)."""
import io, sys, time
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
from coldplate import solve

SW = 200
rows = []
for nx, ny in [(40, 20), (80, 40), (160, 80), (240, 120)]:
    t = time.time()
    r = solve(nx, ny, SW)
    rows.append((nx*ny, r['wall_s']))
    print(f"GRID {nx}x{ny}: cells={nx*ny:7d}  wall={r['wall_s']:8.2f} s  "
          f"({r['wall_s']/(nx*ny*SW)*1e6:.1f} us per cell per sweep)", flush=True)
print("\n-- scaling --")
for i in range(1, len(rows)):
    c0, t0 = rows[i-1]; c1, t1 = rows[i]
    print(f"cells x{c1/c0:.1f} -> time x{t1/t0:.2f}  (exponent {np.log(t1/t0)/np.log(c1/c0):.2f})" if False else
          f"cells x{c1/c0:.1f} -> time x{t1/t0:.2f}")
