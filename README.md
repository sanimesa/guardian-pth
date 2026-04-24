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
git clone https://github.com/sanimesa/guardian-pth
cd guardian-pth
pip install .
```
*Note: The installation automatically deploys the `.pth` hook to your site-packages. No manual copying required.*

### 2. Create a Hardware-Bound Vault
Convert your existing `.env` secrets into an encrypted vault locked to your machine:
```bash
# This will create shadow.vault in the current directory
python3 src/guardian_pth/vault.py import "" shadow.vault .env --hw-bind
```
*Note: You can now safely delete your `.env` file.*

### 3. Update or Add New Secrets
You can add more secrets to an existing vault at any time:
```bash
# Add a single secret via JSON
python3 src/guardian_pth/vault.py update "" shadow.vault '{"NEW_KEY": "new_value"}' --hw-bind

# Or import from another .env file
python3 src/guardian_pth/vault.py import "" shadow.vault additional.env --hw-bind
```

### 4. Verify
Any Python script run in a directory containing `shadow.vault` will now have its environment automatically hydrated.

## Features
- **Zero-Touch Installation**: Automatically deploys the startup hook.
- **Zero-Touch Hydration**: No need to call `load_dotenv()` or modify your application code.
- **Relative Path Support**: Automatically looks for `shadow.vault` in the current working directory.
- **Hardware Binding**: Semi-immutable machine properties (Linux machine-id, etc.) serve as the decryption key.
- **Migration Utility**: Easily import existing `.env` files.

---
*Developed by Shuvro & Paprika 🌶️*
