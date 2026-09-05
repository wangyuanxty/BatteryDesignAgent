import json, sys, os
# Find the bda package structure
bda_path = os.path.join(os.path.dirname(__file__), "..", "..", "..", "..", ".claude", "skills", "virtual-battery-factory", "scripts", "bda")
sys.path.insert(0, os.path.normpath(bda_path))
# List bda submodules
import bda
print("bda path:", os.path.dirname(bda.__file__))
# Try to find pyamm-related modules
for root, dirs, files in os.walk(os.path.dirname(bda.__file__)):
    for f in files:
        if f.endswith(".py") and ("pyamm" in f.lower() or "param" in f.lower()):
            print(os.path.relpath(os.path.join(root, f), os.path.dirname(bda.__file__)))
