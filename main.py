from scraper import PyCurlSynchronousEngine, Request
from lxml import etree


def main():
    with PyCurlSynchronousEngine() as engine:
        res = engine.send(Request('https://en.wikipedia.org/wiki/Elizabeth_II'))

        title = res.xfirst('//h1/text()')
        chapters = []

        # Get Intro
        chapters.append({
            'name': 'Introduction',
            'content': res.xall("//table[contains(@class,'vcard')]/following-sibling::h2[1]/preceding-sibling::p")
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
                'content': res.xall("//h2[./span/text()='{}']/following-sibling::p[following-sibling::h2[./span/text()='{}']]".format(prev_h2, next_h2))
            })

        # from pprint import pprint
        # pprint(chapters)

        # etree.tostring(ele, pretty_print=True).decode()

        # Extract sub chapter (h3)
        # TODO

        # Clean Up each chapter
        # Remove References
        for chapter in chapters:
            for sub_chapter in chapter['content']:
                for link in sub_chapter.xpath('//a'):
                    link.drop_tree()

                    print(sub_chapter.xpath('./text()'))


        # Get all images
        # Can be done on the root


        # Replace link
        # Remove table
        # Remove left over tags

        # Add ssml to title and chapters

        # Write file

        print(content)
        print(title, file=open('output.txt', mode='a'))
        print(intro, file=open('output.txt', mode='a'))



if __name__ == '__main__':
    main()
