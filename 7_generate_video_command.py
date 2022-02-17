import argparse
import os

"""
ffmpeg \
-f lavfi -i color=c=black:s=1920x1080:r=24 \
-i var/Galatia/audio/output_2.wav \
-i var/Galatia/images/001.jpg \
-i var/Galatia/images/002.jpg \
-filter_complex "\
overlay=enable='between(t,0,8)',\
overlay=enable='between(t,8,15)'" \
-c:a copy \
-pix_fmt yuvj422p \
-crf 17 \
-shortest \
out2.mkv

"""

base_command = """
ffmpeg \\
-f lavfi -i color=c=black:s=1920x1080:r=24 \\
-i {audio_path} \\
{images_paths} \\
-filter_complex "\\
{images_overlays}" \\
-c:a aac \\
-pix_fmt yuvj422p \\
-crf 17 \\
-shortest \\
"{folder}/output.mp4"
"""


def main(folder):
    images_timepoints = '{}/timepoints/images.txt'.format(folder)
    images_filenames = sorted(next(os.walk('{}/images'.format(folder)), (None, None, []))[2])
    audio_duration = round(float(os.popen('soxi -D "{}/audio/full.wav"'.format(folder)).read().strip()), 2)

    images_paths = []
    images_overlays = []

    images_timepoints_map = {}

    with open(images_timepoints, mode='r') as file:
        for line in file:
            name, seconds = line.split(' => ')
            number = name[3:]  # Keep the last 3 char
            images_timepoints_map[number] = round(float(seconds), 2)

    start_timestamp = 0
    for image in images_filenames:
        images_paths.append('-i "{}/images/{}"'.format(folder, image))
        next_number = int(image.split('.')[0]) + 1
        end_timestamp = images_timepoints_map.get('{}'.format(next_number))
        if not end_timestamp:
            end_timestamp = audio_duration

        images_overlays.append("overlay=enable='between(t,{},{})'".format(start_timestamp, end_timestamp))
        start_timestamp = end_timestamp

    arguments = {
        'audio_path': '"{}/audio/full.wav"'.format(folder),
        'images_paths': ' \\\n'.join(images_paths),
        'images_overlays': ',\\\n'.join(images_overlays),
        'folder': folder,
    }
    print(base_command.format(**arguments).strip())


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("folder", help="The raw file path of the ssml file", type=str)
    args = parser.parse_args()
    main(args.folder)
