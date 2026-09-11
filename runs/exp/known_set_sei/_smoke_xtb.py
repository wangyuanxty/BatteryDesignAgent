import sys
sys.path.insert(0, r"D:\research\degradation_prognostics\Battery_Design_Agent\.claude\skills\virtual-battery-factory\scripts")
from bda.simulators.xtb_runner import xtb_single_point
r = xtb_single_point("O=S(=O)(F)F")
print("xtb smoke OK:", r)
