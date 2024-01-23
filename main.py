import sys
from Surnix import Surnix


def main():
    args = sys.argv
    if (len(args) > 2):
        print("Usage: surnix [script]")
    elif len(args) == 2:
        Surnix.run_file(args[1])
    else:
        Surnix.run_prompt()


if __name__ == "__main__":
    main()
