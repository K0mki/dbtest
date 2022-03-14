def convert_from_decimal(number, target=16):
    """
    :param number: positive decimal number to be converted
    :param target: target system (2=binary, 8=octal, 16=hexadecimal, max is 2*26+10
    :return: number in target system
    """
    if number < 0:
        return False

    if target > 62 or target < 2:
        return False

    alphabet = ''.join([str(x) for x in range(0, 10)]) + \
               ''.join([chr(x) for x in range(ord('A'), ord('Z') + 1)]) + \
               ''.join([chr(x) for x in range(ord('a'), ord('z') + 1)])

    res = ''
    if number == 0:
        return "0"

    while number > 0:
        b = number % target
        number = number // target
        res = alphabet[b] + res

    return res  # res[::-1]


