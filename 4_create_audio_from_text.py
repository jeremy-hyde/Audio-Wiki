import os
from os import walk
import argparse
from google.cloud import texttospeech_v1beta1 as texttospeech
from google.cloud.texttospeech_v1beta1 import SynthesizeSpeechRequest


def main(folder):
    create_directories(folder)
    filenames = next(walk('{}/ssml'.format(folder)), (None, None, []))[2]

    for i, file in enumerate(filenames, start=1):
        print('Creating audio of file: {}'.format(file))
        synthesize_text_file(i, '{}/ssml/{}'.format(folder, file), folder)


def create_directories(folder):
    # Create directory
    try:
        os.mkdir("{}/audio".format(folder))
    except FileExistsError:
        pass

    try:
        os.mkdir("{}/timepoints".format(folder))
    except FileExistsError:
        pass


def synthesize_text_file(i, text_file, folder):
    """Synthesizes speech from the input file of text."""
    client = texttospeech.TextToSpeechClient()

    with open(text_file, "r") as f:
        text = f.read()
        input_text = texttospeech.SynthesisInput(ssml=text)

    # Note: the voice can also be specified by name.
    # Names of voices can be retrieved with client.list_voices().

    # Great Britain
    # voice = texttospeech.VoiceSelectionParams(
    #     language_code="en-GB",
    #     name="en-GB-Wavenet-B",
    # )

    # United States
    voice = texttospeech.VoiceSelectionParams(
        language_code="en-US",
        name="en-US-Wavenet-D",
    )

    audio_config = texttospeech.AudioConfig(
        speaking_rate=0.90,
        pitch=0.0,
        volume_gain_db=0.0,
        audio_encoding=texttospeech.AudioEncoding.MP3,
        effects_profile_id=['headphone-class-device']
    )

    response = client.synthesize_speech(
        request={"input": input_text, "voice": voice, "audio_config": audio_config, "enable_time_pointing": [SynthesizeSpeechRequest.TimepointType.SSML_MARK]}
    )

    # The response's audio_content is binary.
    with open("{}/audio/output_{}.mp3".format(folder, i), "wb") as out:
        out.write(response.audio_content)
        print('Audio content written to file "{}/audio/output_{}.mp3"'.format(folder, i))

    with open("{}/timepoints/output_{}.txt".format(folder, i), "w") as out:
        for timepoint in response.timepoints:
            out.write("{} => {}\n".format(timepoint.mark_name, timepoint.time_seconds))
        print('Timepoints content written to file "{}/timepoints/output_{}.mp3"'.format(folder, i))


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("folder", help="The folder file from which to synthesize speech.", type=str)
    args = parser.parse_args()
    main(args.folder)
