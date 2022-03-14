import unittest

from .cvt import convert_from_decimal, convert_to_decimal, ExceptionNumberMustBePositive, ExceptionCharacterIsNotValid, ExceptionInvalidTargetRange


class TestConvertFromDecimal(unittest.TestCase):
    def test_cvt_FF_in_16_expected_255(self):
        self.assertEqual(convert_to_decimal('FF'), 255)

    def test_cvt_64_in_16_expected_100(self):
        self.assertEqual(convert_to_decimal('64'), 100)

    def test_cvt_C8_in_16_expected_200(self):
        self.assertEqual(convert_to_decimal('C8'), 200)

    def test_cvt_377_in_8_expected_255(self):
        self.assertEqual(convert_to_decimal('377', 8), 255)

    def test_cvt_minus377_in_8_expected_ExceptionCharacterIsNotValid(self):
        with self.assertRaises(ExceptionCharacterIsNotValid):
            convert_to_decimal('-377', 8)


class TestCvtToDecimal(unittest.TestCase):
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

    def test_cvt_255_in_45_expected_ExceptionInvalidTargetRange(self):
        with self.assertRaises(ExceptionInvalidTargetRange):
            convert_from_decimal(255, 345)

    def test_cvt_minus_255_in_16_expected_Exception_ExceptionNumberMustBePositive(self):
        with self.assertRaises(ExceptionNumberMustBePositive):
            convert_from_decimal(-255)

    def test_cvt_255_in_minus_16_expected_ExceptionInvalidTargetRange(self):
        with self.assertRaises(ExceptionInvalidTargetRange):
            convert_from_decimal(255, -16)

    def test_cvt_255_in_1_expected_ExceptionInvalidTargetRange(self):
        with self.assertRaises(ExceptionInvalidTargetRange):
            convert_from_decimal(255, 1)


class TestConvertFromDecimalToXAndReturnToDecimal(unittest.TestCase):

    def test1(self):
        # This is not recommended practice because we need test to test this program, but it is commonly used in development

        for i in range(0, 300):
            res = convert_from_decimal(i)
            res2 = convert_to_decimal(res)
            self.assertEqual(res2, i)
            # print(i, res, res2)


if __name__ == '__main__':
    unittest.main()
