import argparse
import os
from os import walk


def main(folder):
    filenames = next(walk('{}/timepoints'.format(folder)), (None, None, []))[2]
    filenames = filter(lambda x: x.startswith('output'), filenames)  # keep only files starting with output

    chapters_file = open('{}/timepoints/chapters.txt'.format(folder), mode='w')
    chapters_file.write('TIMESTAMPS\n')
    images_file = open('{}/timepoints/images.txt'.format(folder), mode='w')

    offset = 0

    for i, filename in enumerate(sorted(filenames), start=1):
        duration = float(os.popen("soxi -D {}/audio/output_{}.wav".format(folder, i)).read().strip())
        print('Audio: {0}/audio/output_{1}.wav - Timepoint: {0}/timepoints/output_{1}.txt, Duration: {2}'.format(folder, i, duration))

        with open('{}/timepoints/{}'.format(folder, filename), mode='r') as file:
            for line in file:
                elements = line.split(' => ')
                timestamp = float(elements[1]) + offset
                if elements[0].startswith('img'):
                    images_file.write(' => '.join((elements[0], str(timestamp))))
                    images_file.write('\n')
                else:
                    minutes = round(timestamp) // 60
                    seconds = round(timestamp) % 60
                    chapters_file.write('{}:{:0>2} - {}'.format(minutes, seconds, elements[0]))
                    chapters_file.write('\n')

        offset += duration

    chapters_file.close()
    images_file.close()


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("folder", help="The raw file path of the ssml file", type=str)
    args = parser.parse_args()
    main(args.folder)
