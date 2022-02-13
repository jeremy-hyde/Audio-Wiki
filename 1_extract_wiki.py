import os
import argparse
import shutil
from typing import List

from scraper import PyCurlSynchronousEngine, Request, SynchronousExporter, Settings


# Exemples
#WIKI_PAGE = 'https://en.wikipedia.org/wiki/History_of_Athens'
#WIKI_PAGE = 'https://en.wikipedia.org/wiki/Cyrus_the_Great'
#WIKI_PAGE = 'https://en.wikipedia.org/wiki/Elizabeth_II'


def create_directories(title):
    try:
        shutil.rmtree("var/{}".format(title))
    except FileNotFoundError:
        pass

    # Create directory
    try:
        os.mkdir("var/{}".format(title))
    except FileExistsError:
        pass

    try:
        os.mkdir("var/{}/images".format(title))
    except FileExistsError:
        pass


def clean_up(element):
    for sup in element.xpath('.//sup[not(text() = "2" or text() = "3")]'):
        sup.drop_tree()
    return element.text_content().strip().replace("\u00A0", " ").replace('[edit]', '')


def get_img_url(url):
    if 'thumb' in url:
        src_split: List[str] = url.split('/')
        src_split.pop()  # remove last part
        src_split.remove('thumb')
        return "https:{}".format("/".join(src_split))

    # If the picture has the same size as the original ?
    return "https:{}".format(url)


def extract_caption(element):
    if element.xfirst(".//div[@class='thumbcaption']", suppress_warning=True) is not None:
        return element.xfirst(".//div[@class='thumbcaption']")
    # elif element.xfirst("./div/div[@class='thumbcaption']", suppress_warning=True) is not None:
    #     return element.xfirst("../following-sibling::div[@class='thumbcaption']").text_content()


def main(url):
    settings = Settings()
    settings.remove_http_middleware("RequestFilterMiddlewareHttp")
    settings.remove_http_middleware("HttpHistoryOnSQLiteMiddlewareHttp")
    settings.remove_http_middleware("RetryMiddlewareHttp")
    with PyCurlSynchronousEngine(settings=settings) as engine, SynchronousExporter() as exporter:
        res = engine.send(Request(url))
        print(res)

        print("Extract Titles & Chapters")

        title = res.xfirst('//h1/text()')
        create_directories(title)

        result = [
            title,
            '<break time="1s"/><mark name="Introduction"/><emphasis level="moderate">Introduction.</emphasis><break time="1s"/>'
        ]

        images = []

        images_caption = []

        content = res.xfirst('//div[@class="mw-parser-output"]')
        for element in content.xpath('./*'):
            if element.tag == 'p':
                # remove reference <sup> except if it contains 2 or 3 (km², surface, volume, ...)
                for sup in element.xpath('.//sup[not(text() = "2" or text() = "3")]'):
                    sup.drop_tree()

                result.append(clean_up(element))
            elif element.tag == 'h2':
                h2 = clean_up(element)
                text = '<break time="1s"/><mark name="{0}"/><emphasis level="moderate">{0}.</emphasis><break time="1s"/>'.format(h2)
                result.append(text)
            elif element.tag == 'h3':
                h3 = clean_up(element)
                text = '<break time="0.75s"/><emphasis level="moderate">{0}.</emphasis><break time="0.75s"/>'.format(h3)
                result.append(text)
            elif element.tag == 'h4':
                h4 = clean_up(element)
                text = '<break time="0.5s"/><emphasis level="moderate">{0}.</emphasis><break time="0.5s"/>'.format(h4)
                result.append(text)
            elif element.tag == 'div' and "thumb" in element.get('class', ''):  # Get images
                # Add mark for images here
                image_src = element.xfirst(".//img/@src")
                images.append(get_img_url(image_src))
                description = clean_up(extract_caption(element)).replace('\n', ' ')
                images_caption.append(description)
            else:
                print('Skip element: {}'.format(element.tag))

        # Write results

        print("Write Result File")
        with open('var/{}/raw.txt'.format(title), mode='w') as file:
            file.write('\n'.join(result))

        print("Write Image Caption")
        with open('var/{}/images.txt'.format(title), mode='w') as file:
            file.write('\n'.join(images_caption))

        filepath = 'var/{}/images'.format(title)
        for i, url in enumerate(images, start=1):
            res_img = engine.send(Request(url))
            print(res_img)
            filename = '{:0>3}'.format(i)
            exporter.export_as_file(res_img, filepath, filename)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("url", help="url of the wiki page", type=str)
    args = parser.parse_args()
    main(args.url)
