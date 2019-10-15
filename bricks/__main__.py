from .tests.ard import main as ard
from .tests.ard_emu import main as ard_emu
from .tests.rpi import main as rpi
from .tests.cv import main as cv
import argparse


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("dev", help="Display device")
    parser.add_argument("--port", help="Arduino port", nargs="?")
    args = parser.parse_args()
    if args.dev == "ard":
        print("Using Arduino display")
        if args.port is None:
            print("Provide port")
        else:
            ard(args.port)
    elif args.dev == "ard_emu":
        print("Using Arduino emulator")
        ard_emu()
    elif args.dev == "rpi":
        print("Using RPi display")
        rpi()
    elif args.dev == "cv":
        print("Using CV display")
        cv()
    else:
        print("No such display device")


if __name__ == '__main__':
    main()
