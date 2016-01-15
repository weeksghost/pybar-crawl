import os
from fabric.api import local


urlfile = os.getcwd() + '/links.txt'

def _clean_url_file():
    """Usage -> Erase links to get fresh links

    """
    with open(urlfile, 'w+') as cleaned:
        cleaned.seek(0)
        cleaned.truncate()

def get_urls(url='', depth=''):
    """Usage -> fab get_urls:'<URL>' Fetch major urls from site

    """
    _clean_url_file()
    local('python getlinks.py {url} {depth}'.format(url=url,
                                                depth=depth))
