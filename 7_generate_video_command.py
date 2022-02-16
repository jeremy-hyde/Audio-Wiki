import argparse


def main():
    pass


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("folder", help="The raw file path of the ssml file", type=str)
    args = parser.parse_args()
    main(args.folder)