# Project Charter: Guardian-PTH (Environment Guard)

## Vision
To flip the script on Python's `.pth` file vulnerability, transforming a common attack vector into a robust defense mechanism. This project aims to prevent secret exfiltration by decoupling sensitive environment variables from local files (`.env`) and dynamically injecting them from a secure vault at runtime using site-start hooks.

## Problem Statement
Malicious Python packages often use `.pth` files to execute code immediately upon interpreter startup. This code typically scrapes the local filesystem for `.env`, `config.yaml`, or `.aws/credentials` files and exfiltrates them. Standard "security" measures that rely on local encryption still leave a trace that attackers can target.

## Proposed Solution: The "Shadow Environment"
Instead of storing secrets in files that can be scraped:
1.  **Vault Integration:** Store all sensitive keys in a secure, authenticated vault.
2.  **Stealth Injection:** Deploy a custom `.pth` file in the Python `site-packages` directory.
3.  **Runtime Hydration:** This file will execute on startup, fetch secrets from the vault, and populate `os.environ` dynamically.
4.  **Hardware Binding:** Optionally lock the vault to the semi-immutable properties (Hostname, Machine-ID) of the local machine to prevent decryption on stolen hardware.

## Scope
- **Phase 1:** Core `.pth` logic and local encrypted vault prototype. (COMPLETED)
- **Phase 2:** Support for hardware-bound "Zero-Knowledge" decryption. (COMPLETED)
- **Phase 3:** CLI for managing "Shadow" environments and `.env` migrations. (COMPLETED)
- **Phase 4:** Anti-tamper checks and obfuscation of the hook.

## Success Criteria
- No sensitive keys are stored in plaintext on the local filesystem within the project root.
- Python applications seamlessly access required environment variables via `os.environ`.
- Malicious exfiltration scripts targeting `.env` files find only empty or decoy data.

## Stakeholders
- **Lead Developer:** Shuvro
- **System Architect/Assistant:** Paprika 🌶️
