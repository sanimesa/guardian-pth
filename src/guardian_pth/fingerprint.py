import os
import platform
import subprocess
import hashlib
import base64

def get_machine_fingerprint():
    """
    Collects semi-immutable machine properties to generate a hardware-bound fingerprint.
    Note: These can still be spoofed or change if hardware/OS is reinstalled,
    but they provide a baseline for "zero-knowledge" key derivation.
    """
    components = [
        platform.node(),             # Hostname
        platform.system(),           # OS (Linux/Darwin/Windows)
        platform.machine(),          # Architecture (x86_64)
        # Try to get a unique hardware ID (Linux specific example)
        _get_linux_machine_id()
    ]
    
    # Filter out None and join
    raw_id = "|".join([str(c) for c in components if c])
    return hashlib.sha256(raw_id.encode()).hexdigest()

def _get_linux_machine_id():
    try:
        if os.path.exists("/etc/machine-id"):
            with open("/etc/machine-id", "r") as f:
                return f.read().strip()
        elif os.path.exists("/var/lib/dbus/machine-id"):
            with open("/var/lib/dbus/machine-id", "r") as f:
                return f.read().strip()
    except:
        return None
    return None

if __name__ == "__main__":
    print(f"Machine Fingerprint: {get_machine_fingerprint()}")
