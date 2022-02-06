import argparse
from google.cloud import texttospeech


def synthesize_text_file(text_file, format):
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
    voice = texttospeech.VoiceSelectionParams(
        language_code="en-GB",
        name="en-GB-Wavenet-B",
    )

    audio_config = texttospeech.AudioConfig(
        speaking_rate=1.0,
        pitch=0.0,
        volume_gain_db=0.0,
        audio_encoding=texttospeech.AudioEncoding.MP3,
        effects_profile_id=['headphone-class-device']
    )

    response = client.synthesize_speech(
        request={"input": input_text, "voice": voice, "audio_config": audio_config}
    )

    # The response's audio_content is binary.
    with open("{}/output.mp3".format('/'.join(directories)), "wb") as out:
        out.write(response.audio_content)
        print('Audio content written to file "output.mp3"')


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter
    )
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--text", help="The text file from which to synthesize speech.")
    group.add_argument("--ssml", help="The ssml file from which to synthesize speech.")

    args = parser.parse_args()

    if args.text:
        synthesize_text_file(args.text, 'text')
    else:
        synthesize_text_file(args.ssml, 'ssml')
