#!python3

import sys
import cvt

if __name__ == '__main__':

    if len(sys.argv) < 2:
        print(f"usage {sys.argv[0]} number [base (default=16)]")
        sys.exit(1)

    base = 16

    if len(sys.argv) > 2:
        try:
            base = int(sys.argv[2])
        except:
            print(f"base {sys.argv[1]} is not acceptable")
            sys.exit(3)

    try:
        number = int(sys.argv[1])
    except Exception as e:
        print(f"fnumber {sys.argv[1]} is not acceptable")
        sys.exit(2)

    try:
        print(cvt.convert_from_decimal(number, base))
    except cvt.ExceptionNumberMustBePositive:
        print(f'broj mora biti pozitivan')
        sys.exit(4)
    except cvt.ExceptionCharacterIsNotValid:
        print(f'karakter nije validan')
        sys.exit(5)
    except cvt.ExceptionInvalidTargetRange:
        print(f'range nije validan')
        sys.exit(5)
    except BaseException:
        print(f'nepoznata greska')
        sys.exit(6)

    sys.exit(0)
