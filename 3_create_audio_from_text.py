from os import walk
import argparse
from google.cloud import texttospeech_v1beta1 as texttospeech
from google.cloud.texttospeech_v1beta1 import SynthesizeSpeechRequest


def main(folder, format):
    filenames = next(walk(folder), (None, None, []))[2]

    for i, file in enumerate(filenames, start=1):
        synthesize_text_file(i, file, format)


def synthesize_text_file(i, text_file, format):
    """Synthesizes speech from the input file of text."""

    directories = text_file.split('/')[:-1]  # remove last part

    client = texttospeech.TextToSpeechClient()

    with open(text_file, "r") as f:
        text = f.read()
        if format == 'text':
            input_text = texttospeech.SynthesisInput(text=text)
        else:
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
        speaking_rate=0.95,
        pitch=0.0,
        volume_gain_db=0.0,
        audio_encoding=texttospeech.AudioEncoding.MP3,
        effects_profile_id=['headphone-class-device']
    )

    response = client.synthesize_speech(
        request={"input": input_text, "voice": voice, "audio_config": audio_config, "enable_time_pointing": [SynthesizeSpeechRequest.TimepointType.SSML_MARK]}
    )

    # The response's audio_content is binary.
    with open("{}/audio/output_{}.mp3".format('/'.join(directories), i), "wb") as out:
        out.write(response.audio_content)
        print('Audio content written to file "output.mp3"')

    with open("{}/timepoint/output_{}.txt".format('/'.join(directories), i), "w") as out:
        for timepoint in response.timepoints:
            out.write("{} => {}\n".format(timepoint.mark_name, timepoint.time_seconds))
        print('Timepoints written to file "timepoints.txt"')


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter
    )
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--text", help="The text file from which to synthesize speech.")
    group.add_argument("--ssml", help="The ssml file from which to synthesize speech.")

    args = parser.parse_args()

    if args.text:
        main(args.text, 'text')
    else:
        main(args.ssml, 'ssml')
