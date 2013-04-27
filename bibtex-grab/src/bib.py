#!/usr/bin/env python
# encoding: utf-8
"""
bib.py

Created by Andrew Ning on April 4, 2013
"""

import requests
import sys
from subprocess import Popen, PIPE


# get the DOI
doi = sys.argv[1]

# use REST API (see http://crosscite.org/cn/)
headers = {'Accept': 'application/x-bibtex'}
r = requests.post('http://dx.doi.org/' + doi, headers=headers)

# convert unicode
bibtex = unicode(r.text).encode('utf-8')

# occasionally the record doesn't exist
if bibtex[0] != '@':
    sys.stdout.write('Not Available')
    exit()

# open BibDesk (opens a document if you have this set in BibTeX preferences)
p = Popen(['open', '-a', 'BibDesk'], stderr=PIPE, stdout=PIPE)
p.communicate()


# applescript to import into BibDesk
script = '''
if exists application "BibDesk" then
    tell application "BibDesk"
        activate
        if (count of documents) > 0 then
            tell document 1
                import from "{0}"
            end tell
        end if
    end tell
end if
'''.format(bibtex.replace('"', '\\"'))  # escape quotes

# run applescript
p = Popen(['osascript', '-'], stdin=PIPE, stdout=PIPE)
p.communicate(script)

# pass bibtex
sys.stdout.write(bibtex)

