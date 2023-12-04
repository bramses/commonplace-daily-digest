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
