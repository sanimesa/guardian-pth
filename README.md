# Guardian-PTH: Shadow Environment Guard

**Guardian-PTH** is a security tool designed to neutralize Python supply chain attacks targeting sensitive environment variables. It turns the common `.pth` (path configuration) vulnerability into a defensive "Shadow Environment" mechanism.

## Why this exists
Malicious Python packages often use `.pth` files to execute code the moment the Python interpreter starts. This malicious code typically scans for `.env` files or cloud credentials and exfiltrates them immediately.

**Guardian-PTH** disrupts this by:
1.  **Removing Plaintext Secrets**: Deleting `.env` files entirely.
2.  **Encrypted Vaults**: Storing secrets in an encrypted binary "vault" file.
3.  **Stealth Hydration**: Using its own `.pth` hook to decrypt and inject these secrets directly into `os.environ` in memory at startup.
4.  **Hardware Binding**: Optionally locking the vault to your specific machine's fingerprint (Hostname, OS, and Machine-ID), making stolen vaults useless on other hardware.

## Quick Start

### 1. Installation
```bash
git clone https://github.com/shuvro/guardian-pth
cd guardian-pth
pip install -r requirements.txt
```

### 2. Create a Hardware-Bound Vault
Convert your existing `.env` secrets into an encrypted vault locked to your machine:
```bash
# This will create shadow.vault in the current directory
python3 src/vault.py import "" shadow.vault .env --hw-bind
```
*Note: You can now safely delete your `.env` file.*

### 3. Activate the Hook
Copy the hook trigger to your Python environment's `site-packages`:
```bash
cp src/zzz_guardian.pth $(python3 -m site --user-site)
```

### 4. Verify
Any Python script run in a directory containing `shadow.vault` will now have its environment automatically hydrated without any files being readable by scrapers.

## Features
- **Zero-Touch Hydration**: No need to call `load_dotenv()` or modify your application code.
- **Relative Path Support**: Automatically looks for `shadow.vault` in the current working directory.
- **Hardware Binding**: Semi-immutable machine properties (Linux machine-id, etc.) serve as the decryption key.
- **Migration Utility**: easily import existing `.env` files.

---
*Developed by Shuvro & Paprika 🌶️*
