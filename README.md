# Audio Wiki

Requirements:
pyenv, poetry imagemagick 6.9, inkscape (gives us a svg lib), ffmpeg, sox
Changing imagemagick conf ti increase limits: [see](https://github.com/ImageMagick/ImageMagick/issues/396)

## Documentation
[Google: https://cloud.google.com/text-to-speech/docs/libraries](https://cloud.google.com/text-to-speech/docs/libraries)

## Commands:

### 1. Extract Article
Extract the page into ssml
```shell
python 1_extract_wiki {wiki_article_url}
```

### 2. Split file into smaller files
Split the file in files under 5000 characters for google tts
```shell
python 2_split_file_into_smaler_files.py {path}
```

The following command check the character size of each file
```shell
wc -c {path}/ssml/part_*.txt
```

### 3. Modify Images
This convert, resize and add caption to images
```shell
bash 3_modify_images.bash {path}
```

### 4. Create audio file
```shell
export GOOGLE_APPLICATION_CREDENTIALS=turnkey-axiom-340516-01493ce37939.json
python 4_create_audio_from_text.py --ssml {path}
```

The following command check the length of each file (in seconds)
```shell
soxi -D {path}/audio/output_*.wav
```

### 5. Concatenate audio files
```shell
bash 5_concat_audio.bash {path}
```

### 6. Generate full timepoints
```shell
python 6_filter_and_concat_timepoints.py {path}
```

### 7. Create Video
This command will print another command to execute
```shell
python 7_generate_video_command.py {path}
```

### 8. Create Description
```shell

```
