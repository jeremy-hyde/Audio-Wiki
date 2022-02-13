import argparse
import os

CHARACTER_LIMIT = 5000


def main(folder):
    result_folder = "{}/ssml".format(folder)

    try:
        os.mkdir(result_folder)
    except FileExistsError:
        pass

    file_number = 1
    total = 0
    lines = []
    limit = CHARACTER_LIMIT - 15  # 15 => the tags <speak> </speak>

    with open('{}/raw.txt'.format(folder), mode='r') as file:
        for line in file:
            if total + len(line) < limit:
                lines.append(line)
                total += len(line)
                limit -= 1
            else:
                write_file(file_number, lines, result_folder)

                total = len(line)
                lines = [line]
                file_number += 1
                limit = CHARACTER_LIMIT

        write_file(file_number, lines, result_folder)


def write_file(file_number, lines, result_folder):
    with open('{}/part_{}.txt'.format(result_folder, file_number), mode='w') as file_written:
        file_written.write('<speak>')
        file_written.writelines(lines)
        file_written.write('</speak>')


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("folder", help="The raw file path of the ssml file", type=str)
    args = parser.parse_args()
    main(args.folder)
