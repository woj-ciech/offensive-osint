import json
import requests
from bs4 import BeautifulSoup
from elasticsearch import Elasticsearch

# es = Elasticsearch()

# es.indices.create(index='articles_polityka', ignore=400)

headers = {"Accept":"text/html,application/xhtml+xml aplication/xml;q=0.9,*/*;q=0.8",
           "Accept-Encoding":"gzip, deflate, br",
           "Accept-Language":"""en - US, en;q = 0.5""",
           "User-Agent":"Mozilla/5.0 (X11; Linux x86_64) Gecko/20100101 Firefox/68.0"}


return_dict = {}
def get_articles_id():
    end = "https://www.wykop.pl/ajax2/tag/znaleziska/polityka/wszystkie/next/link-5422543" # https://www.wykop.pl/ajax2/tag/znaleziska/wybory/najlepsze/next/link-5436809

    article_id = ""
    last_id = ""
    req = requests.get(end, headers=headers)

    req_json = json.loads(req.text[8:])
    try:
        soup = BeautifulSoup(req_json['operations'][0]['data'])

        for i in soup.find_all("div",{"data-type":"link"}):
            return_dict = {}
            article_id = i.attrs['data-id']
            timestamp = i.contents[5].contents[7].contents[3].contents[1].attrs['datetime']

            print(article_id)
            get_downvotes(article_id, timestamp)

        for i in range(1,80):
            end_next = "https://www.wykop.pl/ajax2/tag/znaleziska/polityka/wszystkie/next/link-" + article_id
            req_next = requests.get(end_next, headers=headers)

            req_json_next = json.loads(req_next.text[8:])
            soup_next = BeautifulSoup(req_json_next['operations'][0]['data'])

            for i in soup_next.find_all("div", {"data-type": "link"}):
                timestamp = i.contents[5].contents[7].contents[3].contents[1].attrs['datetime']
                article_id = i.attrs['data-id']
                print(article_id)
                get_downvotes(article_id, timestamp)
    except Exception as e:
        print(e)

def get_downvotes(article_id, timestamp):
    usernames = []
    end = "https://www.wykop.pl/ajax2/links/downvoters/"+article_id
    req = requests.get(end, headers=headers)
    req_json = json.loads(req.text[8:])
    soup = BeautifulSoup(req_json['operations'][2]['html'])

    for i in soup.find_all("a", href=True):
        usernames.append(i.attrs['title'])
        print(i.attrs['title'])

    print(timestamp)
    return_dict['timestamp'] = timestamp
    return_dict['link'] = article_id
    return_dict['downvotes'] = usernames
    # es.index(index="articles_polityka", body=return_dict)


get_articles_id()
print(return_dict)
