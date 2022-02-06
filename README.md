

Requirements:

pyenv, poetry imagemagick 6.9, inkscape (gives us a svg lib)

# Documentation
[Google: https://cloud.google.com/text-to-speech/docs/libraries](https://cloud.google.com/text-to-speech/docs/libraries)

## Commands:

### 1. Extract Article
```shell
python extract_wiki {wiki_article_url}
```

### 2. Convert SVG to PNG
```shell
mogrify -format png "var/{page_name}/*.svg" -channel RGB *.png
```

### 3. Create audio file
```shell
export GOOGLE_APPLICATION_CREDENTIALS=turnkey-axiom-340516-01493ce37939.json
python create_audio_from_text.py --text {path}/raw.txt
```