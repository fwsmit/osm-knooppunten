import argparse as arg
from _version import __version__

def main():
    parser = arg.ArgumentParser()
    parser.add_argument('--version', action='version', version='%(prog)s {version}'.format(version=__version__))
    parser.parse_args()

if __name__ == "__main__":
    main()
