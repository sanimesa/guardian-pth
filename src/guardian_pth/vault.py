import os
import json
import base64
import hashlib
import platform
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC

def get_machine_fingerprint():
    """Generates a hardware-bound fingerprint."""
    def _get_linux_machine_id():
        try:
            for p in ["/etc/machine-id", "/var/lib/dbus/machine-id"]:
                if os.path.exists(p):
                    with open(p, "r") as f:
                        return f.read().strip()
        except: pass
        return None

    components = [platform.node(), platform.system(), platform.machine(), _get_linux_machine_id()]
    raw_id = "|".join([str(c) for c in components if c])
    return hashlib.sha256(raw_id.encode()).hexdigest()

def get_key(passphrase: str, salt: bytes) -> bytes:
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt,
        iterations=100000,
    )
    return base64.urlsafe_b64encode(kdf.derive(passphrase.encode()))

def encrypt_secrets(passphrase: str, secrets: dict, output_path: str, use_hw_binding: bool = False):
    if use_hw_binding:
        passphrase = passphrase + get_machine_fingerprint()
    
    salt = os.urandom(16)
    key = get_key(passphrase, salt)
    f = Fernet(key)
    
    encrypted_data = f.encrypt(json.dumps(secrets).encode())
    
    with open(output_path, 'wb') as f_out:
        # We store a flag byte (0x01 for HW bound, 0x00 for standard)
        f_out.write(bytes([1 if use_hw_binding else 0]) + salt + encrypted_data)

def decrypt_secrets(passphrase: str, input_path: str) -> dict:
    with open(input_path, 'rb') as f_in:
        header = f_in.read(1)
        use_hw_binding = header[0] == 1
        data = f_in.read()
        salt, encrypted_data = data[:16], data[16:]
        
    if use_hw_binding:
        passphrase = passphrase + get_machine_fingerprint()
        
    key = get_key(passphrase, salt)
    f = Fernet(key)
    return json.loads(f.decrypt(encrypted_data).decode())

def update_vault(passphrase: str, input_path: str, new_secrets: dict, use_hw_binding: bool = None):
    """
    Decrypts existing vault, merges with new secrets, and re-encrypts.
    If use_hw_binding is not specified, it preserves the existing setting.
    """
    if os.path.exists(input_path):
        with open(input_path, 'rb') as f_in:
            header = f_in.read(1)
            existing_hw_binding = header[0] == 1
        current_secrets = decrypt_secrets(passphrase, input_path)
    else:
        existing_hw_binding = False
        current_secrets = {}

    current_secrets.update(new_secrets)
    
    binding = use_hw_binding if use_hw_binding is not None else existing_hw_binding
    encrypt_secrets(passphrase, current_secrets, input_path, use_hw_binding=binding)

def import_from_env(passphrase: str, vault_path: str, env_path: str, use_hw_binding: bool = None):
    """Parses a .env file and imports secrets into the vault."""
    secrets = {}
    with open(env_path, 'r') as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith('#'):
                continue
            if '=' in line:
                k, v = line.split('=', 1)
                # Strip quotes if present
                v = v.strip().strip("'").strip('"')
                secrets[k.strip()] = v
    
    update_vault(passphrase, vault_path, secrets, use_hw_binding=use_hw_binding)
    return len(secrets)

if __name__ == "__main__":
    import sys
    if len(sys.argv) < 5:
        print("Usage:")
        print("  python vault.py encrypt <passphrase> <path> <json_secrets> [--hw-bind]")
        print("  python vault.py update  <passphrase> <path> <json_secrets> [--hw-bind]")
        print("  python vault.py import  <passphrase> <path> <env_file_path> [--hw-bind]")
        print("  python vault.py decrypt <passphrase> <path>")
        sys.exit(1)
        
    action, pw, path = sys.argv[1], sys.argv[2], sys.argv[3]
    hw_bind = "--hw-bind" in sys.argv

    if action == "encrypt":
        target = sys.argv[4]
        encrypt_secrets(pw, json.loads(target), path, use_hw_binding=hw_bind)
        print(f"Vault created at {path} (Hardware Binding: {hw_bind})")
    elif action == "update":
        target = sys.argv[4]
        update_vault(pw, path, json.loads(target), use_hw_binding=hw_bind if "--hw-bind" in sys.argv else None)
        print(f"Vault updated at {path}")
    elif action == "import":
        target = sys.argv[4]
        count = import_from_env(pw, path, target, use_hw_binding=hw_bind if "--hw-bind" in sys.argv else None)
        print(f"Imported {count} secrets from {target} into {path}")
    elif action == "decrypt":
        print(decrypt_secrets(pw, path))
