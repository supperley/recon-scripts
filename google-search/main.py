"""
Collects links for the specified query in search engines
"""
import json
import time
import requests
from googlesearch import search
from googleapiclient.discovery import build
import config


def google_search_old(search_term):
    return list(search(search_term, stop=1))[0]


def google_search(search_term, api_key, cse_id, **kwargs):
    service = build("customsearch", "v1", developerKey=api_key)
    res = service.cse().list(q=search_term, cx=cse_id, **kwargs).execute()
    return res


def yandex_search(search_term):
    y_url = 'https://yandex.ru/search/xml?params' \
            '&query=' + search_term
    response = requests.get(y_url)
    if response.ok:
        print('page is ok')
        print(response.text)
    return response.text


def serper(search_term):
    url = "https://google.serper.dev/search"

    payload = json.dumps({
        "q": f"{search_term}",
        "gl": "us",
        "hl": "en",
        "autocorrect": True
    })
    headers = {
        'X-API-KEY': f'{SERPER_API}',
        'Content-Type': 'application/json'
    }

    response = requests.request("POST", url, headers=headers, data=payload)

    return response.json()


def main():
    file_in = open("input.txt", "r", encoding="utf-8")
    file_out = open("output.txt", "a")
    lines = file_in.readlines()
    list_of_search_terms = [line.rstrip('\n') for line in lines]
    # print(list_of_search_terms)
    # list_of_search_terms = ['test']  # should be commented
    my_api_key = "my_api_key"
    my_cse_id = "my_cse_id"
    blacklist = ['wikipedia.org', 'instagram.com', 'vk.com', 'rbc', 'interfax.ru',
                 'rbc.ru', 'bloomberg.com', 'kinopoisk.ru', '.ua', '.gov']

    for term in list_of_search_terms:
        try:
            print("Trying to fetch info about: " + term)
            # results = google_search_old(term)
            # results = google_search(term, my_api_key, my_cse_id, num=1)
            # results = yandex_search(term)
            results = serper(term)
            # print(f"Result: {results}")
            idx = 0
            while any(banword in results['organic'][idx]['link'] for banword in blacklist):
                idx += 1

            link = results['organic'][idx]['link']
            print(link)
            file_out.write(f"{link}\n")
            time.sleep(2)
        except Exception as e:
            print("Error: " + str(e))

    file_in.close()
    file_out.close()


if __name__ == '__main__':
    main()
