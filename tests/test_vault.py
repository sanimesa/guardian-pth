import os
import unittest
import shutil
import tempfile
from cryptography.fernet import InvalidToken
from guardian_pth import vault, hook

class TestGuardianVault(unittest.TestCase):
    def setUp(self):
        self.test_dir = tempfile.mkdtemp()
        self.vault_path = os.path.join(self.test_dir, "test.vault")
        self.passphrase = "test-pass"
        self.secrets = {"KEY1": "VAL1", "KEY2": "VAL2"}

    def tearDown(self):
        shutil.rmtree(self.test_dir)
        if "KEY1" in os.environ: del os.environ["KEY1"]
        if "KEY2" in os.environ: del os.environ["KEY2"]

    def test_encrypt_decrypt(self):
        vault.encrypt_secrets(self.passphrase, self.secrets, self.vault_path)
        decrypted = vault.decrypt_secrets(self.passphrase, self.vault_path)
        self.assertEqual(self.secrets, decrypted)

    def test_update_vault(self):
        vault.encrypt_secrets(self.passphrase, self.secrets, self.vault_path)
        new_secrets = {"KEY3": "VAL3"}
        vault.update_vault(self.passphrase, self.vault_path, new_secrets)
        decrypted = vault.decrypt_secrets(self.passphrase, self.vault_path)
        self.assertEqual(decrypted["KEY3"], "VAL3")
        self.assertEqual(decrypted["KEY1"], "VAL1")

    def test_hw_binding_consistency(self):
        # Encrypt with HW binding
        vault.encrypt_secrets(self.passphrase, self.secrets, self.vault_path, use_hw_binding=True)
        # Decrypt on same machine should work
        decrypted = vault.decrypt_secrets(self.passphrase, self.vault_path)
        self.assertEqual(self.secrets, decrypted)

    def test_hydration(self):
        vault.encrypt_secrets(self.passphrase, self.secrets, self.vault_path)
        os.environ["GUARDIAN_VAULT_PATH"] = self.vault_path
        os.environ["GUARDIAN_VAULT_KEY"] = self.passphrase
        hook._hydrate_shadow_env()
        self.assertEqual(os.environ.get("KEY1"), "VAL1")
        self.assertEqual(os.environ.get("KEY2"), "VAL2")

    def test_wrong_passphrase_fails_decrypt(self):
        vault.encrypt_secrets(self.passphrase, self.secrets, self.vault_path)
        with self.assertRaises(InvalidToken):
            vault.decrypt_secrets("wrong-pass", self.vault_path)

    def test_hw_binding_mismatch_fails_decrypt(self):
        vault.encrypt_secrets(self.passphrase, self.secrets, self.vault_path, use_hw_binding=True)
        original = vault.get_machine_fingerprint
        vault.get_machine_fingerprint = lambda: "different-machine"
        try:
            with self.assertRaises(InvalidToken):
                vault.decrypt_secrets(self.passphrase, self.vault_path)
        finally:
            vault.get_machine_fingerprint = original

    def test_malformed_vault_fails_decrypt(self):
        with open(self.vault_path, "wb") as f:
            f.write(b"\x00")
        with self.assertRaises(InvalidToken):
            vault.decrypt_secrets(self.passphrase, self.vault_path)

if __name__ == "__main__":
    unittest.main()
