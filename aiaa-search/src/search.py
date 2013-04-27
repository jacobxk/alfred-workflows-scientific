#!/usr/bin/env python
# encoding: utf-8
"""
search.py

Created by Andrew Ning on April 15, 2013
"""

import requests
from bs4 import BeautifulSoup
import alfred
import sys


# get query from user
query = sys.argv[1]

# grab search data
params = {'searchText': query}
r = requests.get('http://arc.aiaa.org/action/doSearch', params=params)
soup = BeautifulSoup(r.text)
articles = soup.find_all('table', {'class': 'articleEntry'})

results = []

for art in articles:

    # get title
    title = art.find('div', {'class': 'art_title'}).contents[0]

    # get authors
    authorblock = art.find_all('a', {'class': 'entryAuthor'})
    authorString = ''
    for auth in authorblock:
        authorString += auth.span.string + ', '

    # get metadata
    meta = art.find('div', {'class': 'art_meta'})
    journal = meta.span.a.string  # meta.find('a', {'class': 'searchResultJournal'}).contents[0]
    info = meta.contents[1]
    doi = info.split(', ')[-1]

    # get citation link
    links = art.find_all('a', {'class': 'ref nowrap'})
    cite = 'http://arc.aiaa.org' + links[0].get('href')

    # get pdf
    pdf = 'http://arc.aiaa.org' + links[1].get('href')

    # pass data (add custom delimiter so I can pass multiple values)
    data_pass = doi + '***' + authorString[:-2]


    results.append(alfred.Item(title=title,
                               subtitle=authorString + journal + info,
                               attributes={'uid': doi, 'arg': data_pass},
                               icon='icon.png'))

alfred.write(alfred.xml(results))

