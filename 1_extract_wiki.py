import os
import argparse
from typing import List

from scraper import PyCurlSynchronousEngine, Request, SynchronousExporter, Settings


# Exemples
#WIKI_PAGE = 'https://en.wikipedia.org/wiki/History_of_Athens'
#WIKI_PAGE = 'https://en.wikipedia.org/wiki/Cyrus_the_Great'
#WIKI_PAGE = 'https://en.wikipedia.org/wiki/Elizabeth_II'


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
        chapters = []

        # Get Intro
        chapters.append({
            'name': '<mark name="Introduction"/><emphasis level="moderate">Introduction.</emphasis><break time="1s"/>',
            'content': res.xall("//div[@id='mw-content-text']/div/p[1]/following-sibling::h2[1]/preceding-sibling::*[self::p or self::blockquote]")
        })

        # Get Chapter names, excluding the last ones (except the first encounter that will be used as delimiter)
        h2s_names = []
        for h2 in res.xall("//div[@id='mw-content-text']/div/p/following-sibling::h2"):
            content = h2.xfirst("./span/text()")
            h2s_names.append(content)
            if content in ['See also', 'Notes', 'Citations']:
                break

        # Get Chapter content
        for prev_h2, next_h2 in zip(h2s_names, h2s_names[1:]):
            chapters.append({
                'name': '<mark name="{}"/><emphasis level="moderate">{}.</emphasis><break time="1s"/>'.format(prev_h2, prev_h2),
                'content': res.xall("//h2[./span/text()='{}']/following-sibling::*[self::p or self::blockquote or self::h3][following-sibling::h2[./span/text()='{}']]".format(prev_h2, next_h2))
            })

        print('Reformat')
        # Remove table TODO
        # Reformat list TODO
        # Remove left over tags TODO

        # Reformat link
        # Reformat italique
        # Reformat quotes
        # Reformat h3
        # Remove References
        for chapter in chapters:
            for sub_chapter in chapter['content']:
                for link in sub_chapter.xpath('.//a'):
                    link.drop_tag()

                for i in sub_chapter.xpath('.//i'):
                    i.drop_tag()

                for quote in sub_chapter.xpath('.//self::blockquote/p'):
                    quote.drop_tag()

                for sub_title in sub_chapter.xpath('.//self::h3/span'):
                    sub_title.drop_tag()

                for sup in sub_chapter.xpath('.//sup'):
                    sup.drop_tree()

        # Create directory
        try:
            os.mkdir("var/{}".format(title))
        except FileExistsError:
            pass

        try:
            os.mkdir("var/{}/images".format(title))
        except FileExistsError:
            pass


        print("Write file")
        # Write Raw file
        with open('var/{}/raw.txt'.format(title), mode='w') as file:
            for chapter in chapters:
                if chapter['content'] is not None:  # If not content we do not write the chapter titles
                    text = chapter['name'].strip().replace("\u00A0", " ").replace('[edit]', '') # Remove nbsp, whitspaces, "edit" before writing
                    file.write(text)
                    file.write('\n')
                    for sub_chapter in chapter['content']:
                        if sub_chapter.xfirst('./text()') is not None:
                            text = sub_chapter.text_content().strip().replace("\u00A0", " ").replace('[edit]', '')  # Remove nbsp, whitspaces, "edit" before writing
                            file.write(text)
                            file.write('\n')

                    file.write('\n')

        print("Fetch all images")
        # Get all images and descriptions
        with open('var/{}/images.txt'.format(title), mode='w') as file:
            has_seen_caption = False
            for i, img_a in enumerate(res.xall("//a[@class='image']"), start=1):
                description = ''
                if img_a.xfirst("./following-sibling::div[@class='thumbcaption']", suppress_warning=True) is not None:
                    description = img_a.xfirst("./following-sibling::div[@class='thumbcaption']").text_content()
                    has_seen_caption = True
                elif img_a.xfirst("../following-sibling::div[@class='thumbcaption']", suppress_warning=True) is not None:
                    description = img_a.xfirst("../following-sibling::div[@class='thumbcaption']").text_content()
                    has_seen_caption = True
                elif img_a.xfirst('../self::td[@class="mbox-image"]', suppress_warning=True) is not None:  # Table with images but wiki internal info box
                    continue
                elif img_a.xfirst('../self::td', suppress_warning=True) is not None:  # Table with images
                    pass  # The description cannot be retrieved
                elif has_seen_caption:
                    break  # If there are no caption it means we reach the bottom of the page. The following images are part of the menus

                src = img_a.xfirst('./img/@src')
                if 'thumb' in src:
                    src_split: List[str] = src.split('/')
                    src_split.pop()  # remove last part
                    src_split.remove('thumb')
                    src = "https:{}".format("/".join(src_split))
                else: # If the picture has the same size as the original ?
                    src = "https:{}".format(src)

                res_img = engine.send(Request(src))
                print(res_img)
                filename = '{:0>3}'.format(i)
                filepath = 'var/{}/images'.format(title)

                # Save images
                exporter.export_as_file(res_img, filepath, filename)
                # Save description
                file.write(description)
                file.write('\n')


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("url", help="url of the wiki page", type=str)
    args = parser.parse_args()
    main(args.url)
