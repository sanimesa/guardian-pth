# Guardian-PTH Enhancement Plan

## P0: Critical Fixes & Reliability
1.  **Fix `.pth` Syntax:** Rewrite `zzz_guardian.pth` to use a valid single-line syntax:
    `import sys; exec("try:\n    from guardian_pth import hook\n    hook._hydrate_shadow_env()\nexcept Exception: pass")`
    *Or better:* Keep the hook simple and move all error handling into `hook._hydrate_shadow_env()`.
2.  **Test Suite:** Create `tests/test_vault.py` covering:
    *   Vault CRUD (Create, Read, Update, Import).
    *   Hardware binding success/fail.
    *   Environment hydration simulation.

## P1: Security Hardening
3.  **Strict Key Enforcement:** Update `hook.py` to abort if `GUARDIAN_VAULT_KEY` is missing *unless* the vault header explicitly allows "unprotected" HW-only mode.
4.  **Vault Magic & Versioning:** Add a 4-byte magic header (`GPTH`) and a version byte to the vault format to prevent parsing junk and allow for future format upgrades.
5.  **KDF Hardening:** Increase PBKDF2 iterations to 600,000 (OWASP recommendation) and add a `VAULT_VERSION` check to support migration to Argon2id in the next phase.

## P2: DX & Reliability
6.  **Debug Mode:** Implement `GUARDIAN_DEBUG=1` to print errors to stderr during hydration instead of failing silently.
7.  **Modern Packaging:**
    *   Introduce `pyproject.toml`.
    *   Define a CLI entry point: `guardian-vault` for the `vault.py` utility.
8.  **Multi-OS Fingerprinting:**
    *   **macOS:** Use `ioreg -rd1 -c IOPlatformExpertDevice` for UUID.
    *   **Windows:** Use `wmic csproduct get uuid` or registry keys.
9.  **Threat Model Documentation:** Add a "Security Boundaries" section to the README explicitly stating that this mitigates scraping, not memory inspection or ENV hijacking.

---
**Next Step:** I will begin with the P0 syntax fix for the `.pth` file and the test suite. Ready to proceed? 🌶️
