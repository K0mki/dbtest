import unittest

from .cvt import convert_from_decimal


class TestCvt(unittest.TestCase):
    def test_cvt_255_in_16_expected_FF(self):
        self.assertEqual(convert_from_decimal(255), 'FF')

    def test_cvt_100_in_16_expected_64(self):
        self.assertEqual(convert_from_decimal(100), '64')

    def test_cvt_100_in_200_expected_C8(self):
        self.assertEqual(convert_from_decimal(200), 'C8')

    def test_cvt_100_in_222_expected_DE(self):
        self.assertEqual(convert_from_decimal(222), 'DE')

    def test_cvt_255_in_octal_expected_377(self):
        self.assertEqual(convert_from_decimal(255, 8), '377')

    def test_cvt_255_in_45_expected_5U(self):
        self.assertEqual(convert_from_decimal(255, 45), '5U')

    def test_cvt_255_in_45_expected_FALSE(self):
        self.assertFalse(convert_from_decimal(255, 345))

    def test_cvt_minus_255_in_16_expected_FALSE(self):
        self.assertFalse(convert_from_decimal(-255))

    def test_cvt_255_in_minus_16_expected_FALSE(self):
        self.assertFalse(convert_from_decimal(255, -16))

    def test_cvt_255_in_1_expected_FALSE(self):
        self.assertFalse(convert_from_decimal(255, 1))


if __name__ == '__main__':
    unittest.main()
