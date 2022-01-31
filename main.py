import os

from lxml import etree
from scraper import PyCurlSynchronousEngine, Request


def main():
    with PyCurlSynchronousEngine() as engine:
        res = engine.send(Request('https://en.wikipedia.org/wiki/Elizabeth_II'))
        print(res)

        title = res.xfirst('//h1/text()')
        chapters = []

        # Get Intro
        chapters.append({
            'name': 'Introduction',
            'content': res.xall("//table[contains(@class,'vcard')]/following-sibling::h2[1]/preceding-sibling::*[self::p or self::blockquote]")
        })

        # Get Chapter names, excluding the last ones (except the first encounter that will be used as delimiter)
        h2s_names = []
        for h2 in res.xall("//table[contains(@class,'vcard')]/following-sibling::h2"):
            content = h2.xfirst("./span/text()")
            h2s_names.append(content)
            if content in ['See also', 'Notes', 'Citations']:
                break

        # Get Chapter content
        for prev_h2, next_h2 in zip(h2s_names, h2s_names[1:]):
            chapters.append({
                'name': prev_h2,
                'content': res.xall("//h2[./span/text()='{}']/following-sibling::*[self::p or self::blockquote][following-sibling::h2[./span/text()='{}']]".format(prev_h2, next_h2))
            })

        #print(etree.tostring(chapters[3]['content'], pretty_print=True).decode())

        # Extract sub chapter (h3)
        # TODO

        # Remove table TODO
        # Remove left over tags TODO
        # Clean up each chapter
        # Reformat link
        # Reformat italique
        # Reformat quotes
        # Remove References
        for chapter in chapters:
            for sub_chapter in chapter['content']:
                for link in sub_chapter.xpath('.//a'):
                    link.drop_tag()

                for i in sub_chapter.xpath('.//i'):
                    i.drop_tag()

                for quote in sub_chapter.xpath('.//blockquote'):
                    print(quote.xpath('./p/text()'))
                    quote.drop_tag()

                for sup in sub_chapter.xpath('.//sup'):
                    sup.drop_tree()

        # Create directory
        try:
            os.mkdir("var/{}".format(title))
        except FileExistsError:
            pass

        with open('var/{}/raw.txt'.format(title), mode='w') as file:
            for chapter in chapters:
                if chapter['content']:
                    file.write(chapter['name'].strip())
                    file.write('\n\n')
                    for sub_chapter in chapter['content']:
                        if sub_chapter.xfirst('./text()'):
                            file.write(sub_chapter.xfirst('./text()'))
                            file.write('\n\n')

                    file.write('\n\n')


        # Get all images
        # Can be done on the root




        # Add ssml to title and chapters

        # Write file




if __name__ == '__main__':
    main()
