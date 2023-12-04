import requests
import json
import os
import datetime
from dotenv import load_dotenv
load_dotenv()

# Get the token from the .env file
READWISE_ACCESS_TOKEN = os.getenv("READWISE_ACCESS_TOKEN")


def check_token():
    # set the headers
    headers = {
        "Authorization": "Token " + READWISE_ACCESS_TOKEN
    }

    # make the GET request
    response = requests.get(
        "https://readwise.io/api/v2/auth/", headers=headers)

    if response.status_code == 204:
        print("Token is valid")
        return True
    else:
        print("Token is invalid")
        return False


def fetch_from_export_api(updated_after=None):
    full_data = []
    next_page_cursor = None
    while True:
        params = {}
        if next_page_cursor:
            params['pageCursor'] = next_page_cursor
        if updated_after:
            params['updatedAfter'] = updated_after
        print("Making export api request with params " + str(params) + "...")
        response = requests.get(
            url="https://readwise.io/api/v2/export/",
            params=params,
            headers={"Authorization": f"Token {READWISE_ACCESS_TOKEN}"}, verify=False
        )
        full_data.extend(response.json()['results'])
        next_page_cursor = response.json().get('nextPageCursor')
        if not next_page_cursor:
            break
    return full_data


def write_to_file(data, name='data.json', is_json=True):
    with open(name, 'w') as outfile:
        if is_json:
            json.dump(data, outfile, indent=4)
        else:
            print(data, file=outfile)


def read_from_file(name='data.json'):
    with open(name) as json_file:
        data = json.load(json_file)
    return data


def filter_highlights_by_category(highlights, category):
    return [highlight for highlight in highlights if highlight['category'] == category]


def create_articles(data):
    articles = []
    for res in data:
        if res['category'] == 'articles':
            article = {
                'readable_title': res['title'],
                'author': res['author'],
                'source_url': res['source_url'],
                'highlights': []
            }
            for highlight in res['highlights']:
                article['highlights'].append({
                    'text': highlight['text'],
                    'note': highlight['note']
                })
            articles.append(article)
    return articles


def create_books(data):
    books = []
    for res in data:
        if res['category'] == 'books':
            book = {
                'readable_title': res['title'],
                'author': res['author'],
                'amazon_url': "",
                'asin': res['asin'],
                'cover_image_url': res['cover_image_url'],
                'highlights': []
            }
            for highlight in res['highlights']:
                book['highlights'].append({
                    'text': highlight['text'],
                    'note': highlight['note'],
                    'highlighted_at': highlight['highlighted_at']
                })
            books.append(book)
    return books


def main(write_path="", READ_FROM_FILE=False, WRITE_TO_FILE=True, read_path=""):
    new_data = []
    if READ_FROM_FILE:
        new_data = read_from_file(read_path)
    else:
        # midnight today
        # today_str = datetime.date.today().strftime('%Y-%m-%d')
        # DAY_LAST_FETCHED = today_str
        # day_delta = datetime.datetime.now() - datetime.datetime.strptime(DAY_LAST_FETCHED, '%Y-%m-%d')
        # print("Fetching data from the last " + str(day_delta.days) + " days...")

        # last_fetch_was_at = datetime.datetime.combine(datetime.datetime.now().date(), datetime.time())  # use your own stored date
        # print("Last fetch was at " + last_fetch_was_at.isoformat())
        # new_data = fetch_from_export_api(last_fetch_was_at.isoformat())

        # 801pm yesterday
        yesterday = datetime.date.today() - datetime.timedelta(days=1)

        DAY_LAST_FETCHED = yesterday.strftime('%Y-%m-%d')
        day_delta = datetime.datetime.now(
        ) - datetime.datetime.strptime(DAY_LAST_FETCHED, '%Y-%m-%d')
        print("Fetching data from the last " +
              str(day_delta.days) + " days...")

        last_fetch_was_at = datetime.datetime.combine(
            yesterday, datetime.time(20, 1))  # yesterday at 8:01 PM
        print("Last fetch was at " + last_fetch_was_at.isoformat())
        new_data = fetch_from_export_api(last_fetch_was_at.isoformat())


        # filter any highlights in data.res.highlights that are older than yesterday 801pm example date format (new_data.[res].[higlights]."highlighted_at": "2023-11-14T15:41:44.943Z")
        for res in new_data:
            res['highlights'] = [
                highlight for highlight in res['highlights'] if highlight['highlighted_at'] > last_fetch_was_at.isoformat()]
            # print the highlighted_at date for each highlight
            # for highlight in res['highlights']:
            #     print(highlight['highlighted_at'])
            # print("Filtering highlights from " + res['title'] + "...")
            # print("There are " + str(len(res['highlights'])) + " highlights")

    articles = create_articles(new_data)
    books = create_books(new_data)

    joined_data = {
        "articles": articles,
        "books": books
    }

    if WRITE_TO_FILE:
        write_to_file(joined_data, write_path, is_json=True)


if __name__ == "__main__":
    main()
