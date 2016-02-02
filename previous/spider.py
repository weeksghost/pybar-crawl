import os
import sys
import requests
requests.packages.urllib3.disable_warnings()
import urlparse
from bs4 import BeautifulSoup

cur = os.getcwd()
urlfile = cur + '/spider_links.txt'


def page_spider(url, username=None, passwd=None):
    """
    Usage => python previous/spider.py <URL>
    """
    urls = [url]
    visited = [url]
    auth = (username, passwd)

    while len(urls) > 0:
        try:
            request = requests.get(urls[0], auth=auth, verify=False)
            htmltext = request.content
        except:
            raise Exception('Could not aquire: {}'.format(urls[0]))
        soup = BeautifulSoup(htmltext)

        urls.pop(0)
        print(str(len(urls)) + ' links checked out okay')

        for tag in soup.findAll('a', href=True):
            tag['href'] = urlparse.urljoin(url, tag['href'])
            if url in tag['href'] and tag['href'] not in visited:
                urls.append(tag['href'])
                visited.append(tag['href'])
    for link in visited:
        parsed = urlparse.urlparse(link)
        path = parsed.path
        with open(urlfile, 'ab') as data:
            data.write(path)
            print link

page_spider(sys.argv[1])
