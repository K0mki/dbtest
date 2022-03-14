class ExceptionNumberMustBePositive(BaseException):
    pass


class ExceptionCharacterIsNotValid(BaseException):
    pass


class ExceptionInvalidTargetRange(BaseException):
    pass


alphabet = ''.join([str(x) for x in range(0, 10)]) + \
           ''.join([chr(x) for x in range(ord('A'), ord('Z') + 1)]) + \
           ''.join([chr(x) for x in range(ord('a'), ord('z') + 1)])

m_alphabet = {}
pos = -1
for l in alphabet:
    pos += 1
    m_alphabet[l] = pos


def convert_to_decimal(number: str, source=16):
    """
    :param number: number in system (source)
    :param source: (2=binary, 8=octal, 16=hexadecimal, max is 2*26+10)
    :return: number in decimal value
    """

    res = 0
    for c in enumerate(number[::-1]):
        if c[1] not in m_alphabet:
            raise ExceptionCharacterIsNotValid

        res += (source ** c[0]) * m_alphabet[c[1]]

    return res


def convert_from_decimal(number: int, target=16):
    """
    :param number: positive decimal number to be converted
    :param target: target system (2=binary, 8=octal, 16=hexadecimal, max is 2*26+10
    :return: number in target system
    """
    if number < 0:
        raise ExceptionNumberMustBePositive

    if target > 62 or target < 2:
        raise ExceptionInvalidTargetRange

    res = ''
    if number == 0:
        return "0"

    while number > 0:
        b = number % target
        number = number // target
        res += alphabet[b]

    return res[::-1]
