import tempfile
import unittest
from pathlib import Path

from scripts.prepare_env import prepare_env


class PrepareEnvTests(unittest.TestCase):
    def test_generates_unique_secret_for_blank_template(self):
        with tempfile.TemporaryDirectory() as first_dir, tempfile.TemporaryDirectory() as second_dir:
            first = Path(first_dir)
            second = Path(second_dir)
            for root in (first, second):
                (root / ".env.example").write_text(
                    "DJANGO_SECRET_KEY=\nDJANGO_DEBUG=True\n",
                    encoding="utf-8",
                )
                self.assertTrue(prepare_env(root))

            first_content = (first / ".env").read_text(encoding="utf-8")
            second_content = (second / ".env").read_text(encoding="utf-8")
            self.assertNotEqual(first_content, second_content)
            secret_line = next(line for line in first_content.splitlines() if line.startswith("DJANGO_SECRET_KEY="))
            self.assertGreaterEqual(len(secret_line.split("=", 1)[1].strip('"')), 50)

    def test_preserves_existing_nonempty_secret(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            existing = 'DJANGO_SECRET_KEY="existing-local-value"\nDJANGO_DEBUG=True\n'
            (root / ".env").write_text(existing, encoding="utf-8")
            (root / ".env.example").write_text("DJANGO_SECRET_KEY=\n", encoding="utf-8")

            self.assertFalse(prepare_env(root))
            self.assertEqual((root / ".env").read_text(encoding="utf-8"), existing)


if __name__ == "__main__":
    unittest.main()