# -*- coding: utf-8 -*-
import os
import re
import shutil
import tempfile
import unittest

from utils.abogus_pure import generate_abogus


class ABogusPureDirectTest(unittest.TestCase):
    def test_generate_abogus_without_mapping_files(self):
        temp_dir = tempfile.mkdtemp()
        root = os.path.dirname(os.path.dirname(__file__))
        reverse_dir = os.path.join(root, "lib", "reverse")
        mapping_paths = [
            os.path.join(reverse_dir, "time_mapping_full.json"),
            os.path.join(reverse_dir, "time_mapping_sample.json"),
        ]
        moved = []

        try:
            for path in mapping_paths:
                if os.path.exists(path):
                    backup = os.path.join(temp_dir, os.path.basename(path))
                    os.rename(path, backup)
                    moved.append((backup, path))

            signed = generate_abogus(
                "https://www.douyin.com/aweme/v1/web/aweme/detail/?aweme_id=1",
                1704067200000,
            )

            self.assertGreater(len(signed), 80)
            self.assertRegex(signed, r"^[A-Za-z0-9/+\-=]+$")
        finally:
            for backup, path in reversed(moved):
                os.rename(backup, path)
            shutil.rmtree(temp_dir)


if __name__ == "__main__":
    unittest.main()
