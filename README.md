1. At the end of each day, ping the readwise api (READWISE_ACCESS_TOKEN) to get the highlights for the day
2. If there are highlights, create a new note in the /daily folder with the highlights in markdown format
    a. format should be under book header
3. leave placeholders above for thoughts

Book and Article Schema from Readwise:

'''
    [article, article, book, book, book...]

    article schema {
        readable_title: str
        author: str
        source_url: str
        highlights: list[Highlight]
    }

    article.Highlight schema {
        text: str
        note: str
    }

    book schema {
        readable_title: str
        author: str
        amazon_url: str
        cover_image_url: str
        highlights: list[Highlight]
    }
    book.Highlight schema {
        text: str
        note: str
    }
'''

TODO:
- [ ] smart copy to clipboard

```
'''
    generate html for each highlight that creates a button to copy the highlight to the clipboard

    like:
    ...text...

    (COPY TO CLIPBOARD BTN)

    (> copies the below text to the clipboard)
    
    {note}

    > Biologists divide cells and organisms into the genotype (the genetic information) and the phenotype (the enzymes and other proteins, as well as the organs and morphology, that make up the body). With autocatalytic sets, there is no separation between genotype and phenotype. The system serves as its own genome. Nevertheless, the capacity to incorporate novel molecular species, and perhaps eliminate older molecular forms, promises to generate a population of self-reproducing chemical networks with different characteristics. Darwin tells us that such systems will evolve by natural selection.
    -- At Home in the Universe: The Search for the Laws of Self-Organization and Complexity by Stuart A. Kauffman

    from https://www.bramadams.dev/november-21-2023/ (var url = window.location.href;)
    '''
```