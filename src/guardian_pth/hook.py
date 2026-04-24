import os
import sys
import platform
import hashlib
import base64
import json
import subprocess
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC

def get_machine_fingerprint():
    def _get_id():
        try:
            if platform.system() == "Linux":
                for p in ["/etc/machine-id", "/var/lib/dbus/machine-id"]:
                    if os.path.exists(p):
                        with open(p, "r") as f: return f.read().strip()
            elif platform.system() == "Windows":
                cmd = "powershell (Get-CimInstance Win32_ComputerSystemProduct).UUID"
                return subprocess.check_output(cmd, shell=True).decode().strip()
            elif platform.system() == "Darwin":
                cmd = "ioreg -rd1 -c IOPlatformExpertDevice | grep IOPlatformUUID"
                res = subprocess.check_output(cmd, shell=True).decode()
                return res.split('\"')[-2]
        except: pass
        return None
    components = [platform.node(), platform.system(), platform.machine(), _get_id()]
    raw_id = "|".join([str(c) for c in components if c])
    return hashlib.sha256(raw_id.encode()).hexdigest()

def _hydrate_shadow_env():
    # 1. Check for explicit path in environment
    vault_path = os.environ.get("GUARDIAN_VAULT_PATH")
    
    # 2. If not in env, check current directory for a default vault file
    if not vault_path:
        local_default = os.path.join(os.getcwd(), "shadow.vault")
        if os.path.exists(local_default):
            vault_path = local_default
            
    # 3. If still not found, check the hook's own directory (for bundled distribution)
    if not vault_path:
        bundled_default = os.path.join(os.path.dirname(__file__), "shadow.vault")
        if os.path.exists(bundled_default):
            vault_path = bundled_default

    vault_key = os.environ.get("GUARDIAN_VAULT_KEY", "")
    
    if not vault_path or not os.path.exists(vault_path):
        return

    try:
        with open(vault_path, 'rb') as f:
            header = f.read(1)
            use_hw_binding = header[0] == 1
            data = f.read()
            salt, encrypted_data = data[:16], data[16:]

        passphrase = vault_key
        if use_hw_binding:
            passphrase += get_machine_fingerprint()

        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=32,
            salt=salt,
            iterations=100000,
        )
        key = base64.urlsafe_b64encode(kdf.derive(passphrase.encode()))
        f_crypt = Fernet(key)
        secrets = json.loads(f_crypt.decrypt(encrypted_data).decode())
        
        for k, v in secrets.items():
            os.environ[k] = str(v)
            
    except Exception:
        pass

if __name__ == "__main__" or "site" in sys.modules:
    _hydrate_shadow_env()
