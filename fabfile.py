import os
from fabric.api import local


curdir = os.getcwd()
dupes = curdir + '/duplicates.txt'
urlfile = curdir + '/links.txt'

def get_urls(url='', depth=''):
    """Usage -> fab get_urls:'<URL>' Fetch major urls from site

    """
    _clean_files()
    local('python getlinks.py {url} {depth}'.format(url=url,
                                                depth=depth))
    _dedupe()

def _dedupe():
    with open(dupes, 'r+') as duplicates:
        seen = set()
        dedupe = []
        for line in duplicates:
            if line not in seen:
                dedupe.append(line)
                seen.add(line)
        for item in dedupe:
            with open(urlfile, 'ab') as links:
                links.write(item)
                print item.strip()

def _clean_files():
    """Usage -> Erase links to get fresh links

    """
    with open(urlfile, 'w+') as cleaned:
        cleaned.seek(0)
        cleaned.truncate()
    with open(dupes, 'w+') as cleaned:
        cleaned.seek(0)
        cleaned.truncate()
