import unittest

import turkey_postal_codes as tpc
from turkey_postal_codes import normalize, normalize_postal_code


class TestNormalize(unittest.TestCase):
    def test_turkish_case(self):
        self.assertEqual(normalize("İSTANBUL"), normalize("istanbul"))
        self.assertEqual(normalize("IĞDIR"), normalize("ığdır"))
        self.assertEqual(normalize("Deni̇zli̇"), "denizli")

    def test_postal_code(self):
        self.assertEqual(normalize_postal_code(1040), "01040")
        self.assertEqual(normalize_postal_code(" 34519 "), "34519")
        self.assertIsNone(normalize_postal_code("abc"))
        self.assertIsNone(normalize_postal_code("123456"))


class TestLookup(unittest.TestCase):
    def test_get(self):
        res = tpc.get("01040")
        self.assertEqual(res["il"], "Adana")
        self.assertEqual(res["plaka"], 1)

    def test_int_input(self):
        self.assertEqual(tpc.get(1040), tpc.get("01040"))

    def test_shortcuts(self):
        self.assertEqual(tpc.get_city("01040"), "Adana")
        self.assertEqual(tpc.get_district("01040"), "Seyhan")
        self.assertEqual(tpc.get_city("00000", default="?"), "?")

    def test_invalid(self):
        self.assertIsNone(tpc.get("99999x"))
        self.assertFalse(tpc.is_valid("00000"))

    def test_search(self):
        self.assertTrue(tpc.search_by_city("ADANA"))
        self.assertTrue(tpc.search_by_district("adana", "SEYHAN"))
        self.assertIn("01040", tpc.postal_codes_of("Adana", "Seyhan"))
        self.assertIn("Seyhan", tpc.list_districts("Adana"))
        self.assertEqual(tpc.list_cities()[0], "Adana")

    def test_neighborhoods(self):
        self.assertTrue(all(r["posta_kodu"] == "01040" for r in tpc.get_neighborhoods("01040")))


if __name__ == "__main__":
    unittest.main()
