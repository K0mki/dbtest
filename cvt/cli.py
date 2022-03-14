import sys
import argparse

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("echo", help="echo the string you use here")
    parser.add_argument("--verbose", help="print more details what you do", action="store_true")
    parser.add_argument("--base", help="in which base you want to convert number", default=16)
    args = parser.parse_args()

    base = int(args.base)
    if base < 2 or base > 62:
        print(f"invalid base {args.base}")
        sys.exit(1)

    if args.verbose:
        print("zadat argument je ", args.echo)
    else:
        print(args.echo)

    print("BASE",args.base)

