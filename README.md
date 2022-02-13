# Audio Wiki

Requirements:

pyenv, poetry imagemagick 6.9, inkscape (gives us a svg lib)

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

### 3. Create audio file
```shell
export GOOGLE_APPLICATION_CREDENTIALS=turnkey-axiom-340516-01493ce37939.json
python 3_create_audio_from_text.py --ssml {path}
```

### 4. Modify Images
This convert, resize and add caption to images
```shell
bash 4_modify_images.bash {path}
```

### 5. Create Videos
```shell

```

### 6. Create Description
```shell

```
