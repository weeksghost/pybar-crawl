import os
import threading
import urlparse
from bs4 import BeautifulSoup
import requests
requests.packages.urllib3.disable_warnings()


class CategoryThread(threading.Thread):

    cur_dir = os.getcwd()
    url_file = cur_dir + '/links.txt'
    URL_SCHEMA = 'http://'

    def __init__(self, binarySemaphore, url, crawlDepth):
        self.binarySemaphore = binarySemaphore
        url = urlparse.urlparse(url)
        new_url = self.URL_SCHEMA + '%s' % url.netloc
        self.url = new_url
        self.crawlDepth = crawlDepth
        self.threadId = hash(self)
        threading.Thread.__init__(self)

    def run(self):
        urls = [self.url]
        visted = [self.url]

        request = requests.get(self.url, verify=False)
        htmltext = request.content
        soup = BeautifulSoup(htmltext, 'html.parser')

        self.binarySemaphore.acquire()
        urls.pop(0)

        for tag in soup.findAll('a', href=True):
            tag['href'] = urlparse.urljoin(self.url, tag['href'])
            if self.url in tag['href'] and tag['href'] not in visted:
                urls.append(tag['href'])
                visted.append(tag['href'])
        dedupe = list(set(urls))
        new_links = []
        new_file_links = []
        for link in dedupe:
            new_ones = '{link}'.format(link=link)
            new_links.append(new_ones)
            new_file_links.append(link)
        nodupes = list(set(new_file_links))
        with open(self.url_file, 'ab') as url_file:
            for link in nodupes:
                parse = urlparse.urlparse(link)
                if parse.netloc == '':
                    pass
                else:
                    url_file.write(link + '\n')
                    print(link)

        self.binarySemaphore.release()

        new_links = list(set(new_links))
        return new_links

        for url in urls:
            if self.crawlDepth > 1:
                CategoryThread(binarySemaphore, url, self.crawlDepth-1).start()


if __name__ == "__main__":

    binarySemaphore = threading.Semaphore(1)
