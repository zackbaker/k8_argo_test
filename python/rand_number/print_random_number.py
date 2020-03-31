import argparse

if __name__ == "__main__":
    parser = argparse.ArgumentParser('Find random number in file')
    parser.add_argument('file_path', metavar='FILEPATH', type=str, nargs=1, help='Path to file')
    args = parser.parse_args()
    file_path = args.file_path[0]
    file = open(file_path, 'r')
    print('Random number is: ' + str(file.read()))
