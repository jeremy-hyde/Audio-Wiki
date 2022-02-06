

Requirements:

pyenv, poetry imagemagick 6.9, inkscape (gives us a svg lib)

## Commands:

### 1. Extract Article
```shell
python extract_wiki {wiki_article_url}
```

### 2. Convert SVG to PNG
```shell
mogrify -format png "var/{page_name}/*.svg" -channel RGB *.png
```