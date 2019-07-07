from bricks.tests.emu import main as emu_main
from bricks.tests.ard import main as ard_main
import argparse


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--display_port", help="The port where I can find the display", type=str)
    args = parser.parse_args()
    if args.display_port is None:
        emu_main()
    else:
        ard_main(args.display_port)


if __name__ == '__main__':
    main()
