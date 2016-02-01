import requests
requests.packages.urllib3.disable_warnings()
import urlparse
from bs4 import BeautifulSoup


def page_spider(url, username=None, passwd=None):
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

        for tag in soup.findAll('a', href=True):
            tag['href'] = urlparse.urljoin(url, tag['href'])
            if url in tag['href'] and tag['href'] not in visited:
                urls.append(tag['href'])
                visited.append(tag['href'])
        links = []
        for link in visited:
            parsed = urlparse.urlparse(link)
            links.append(parsed.path)
            print link

page_spider('https://storefront:gr34tsk1n@production-web-perriconemd.demandware.net/s/perriconemd', username='storefront', passwd='gr34tsk1n')
#page_spider('https://storefront:gr34tsk1n@staging.perriconemd.com', username='storefront', passwd='gr34tsk1n')
