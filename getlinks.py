import os
import sys
import threading
import urlparse
from bs4 import BeautifulSoup
import requests
requests.packages.urllib3.disable_warnings()

from crawler import CategoryThread


class PDPThread(threading.Thread):

    def __init__(self, binarySemaphore, url, crawlDepth):
        self.binarySemaphore = binarySemaphore
        self.url = url
        self.crawlDepth = int(crawlDepth)
        self.threadId = hash(self)
        threading.Thread.__init__(self)

    def run(self):
        request = requests.get(self.url, verify=False)
        htmltext = request.content
        soup = BeautifulSoup(htmltext, 'html.parser')

        self.binarySemaphore.acquire()

        dupes = []
        seen = set()
        for tag in soup.findAll('a', href=True):
            links = urlparse.urljoin(self.url, tag['href'])
            if links not in seen:
                dupes.append(links)
                seen.add(links)
        for link in dupes:
            with open(os.getcwd() + '/links.txt', 'ab') as getlinks:
                parse = urlparse.urlparse(link)
                if parse.netloc == '':
                    pass
                else:
                    getlinks.write(link.encode('utf-8') + '\n')
                    print(link)

        self.binarySemaphore.release()

        for url in urls:
            if self.crawlDepth > 1:
                PDPThread(binarySemaphore, url, self.crawlDepth-1).start()


if __name__ == "__main__":

    try:
        binarySemaphore = threading.Semaphore(1)
        categories = CategoryThread(binarySemaphore, sys.argv[1], 1)
        urls = categories.run()
        for url in urls:
            PDPThread(binarySemaphore, url, crawlDepth=sys.argv[2]).start()
    except:
        print("\nCheck command format.\nFor example:\n\n" +
                "fab get_urls:'https://www.google.com 1'")
