import json
from urllib.request import urlopen
from urllib.parse import quote

import re


def get_results(query, format='json', n_rows=1000):
    """Gets a Json from dblp API"""
    parse_query = quote(query)
    url = f"https://dblp.org/search/publ/api?q={parse_query}&h={n_rows}&format={format}"
    # store the response of URL
    response = urlopen(url)
    file_result = f'{query}'
    with open(f'{file_result}.{format}', 'w', encoding='utf-8') as f:
        print(f'Writing {file_result}.{format}')
        json.dump(json.loads(response.read()), f, ensure_ascii=False, indent=4)
        print('Done')


def parse_dblp_csv(filename):
    """ Parses dblp json result to csv file"""

    f = open(filename+'.json', encoding="utf8")
    data = json.load(f)
    entries = []

    for h in data['result']['hits']['hit']:
        entry = []
        entry.append(filename)
        entry.append(h['@id'])
        entry.append(h['info']['title'])
        if isinstance(h['info']['authors']['author'], list):
            try:
                entry.append(", ".join([re.sub(r'\d', '', a["text"])
                             for a in h['info']['authors']['author']]))
            except:
                raise ValueError(str(h['info']['authors']['author']))
        else:
            entry.append(
                re.sub(r'\d', '', h['info']['authors']['author']["text"]))
        entry.append(h['info']['year'])
        entry.append(h['info'].get('ee', ""))
        entry.append(h['info'].get('venue', ""))
        entry.append(h['info'].get('publisher', ""))
        entry.append(h['info']['type'])
        entries.append(entry)

    import pandas as pd
    export = pd.DataFrame(entries, columns=[
                          'query', 'id', 'title', 'authors', 'year', 'url', 'venue', 'publisher', 'type'])
    print(f'Writing {filename}_table.csv')
    export.to_csv(filename+'_table.csv', index=False)
    print(f'Done!')


def process_query(query):
    """ Gets the Json file `{query}.json` an parses it to a csv file `{query}_table.csv`"""
    get_results(query)
    parse_dblp_csv(query)


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description='DBLP abductor')
    parser.add_argument('query', type=str, help='dblp valid query')

    args = parser.parse_args()
    query = args.query

    #query = "fair recommend"
    process_query(query)
