import requests
from bs4 import BeautifulSoup
from datetime import datetime
import multiprocessing as mp
import sys
from multiprocessing import freeze_support, Queue


# basic logging. 0 for errors and 1 for non-errors
def logging(msg, code):
    if code == 0:
        with open('web_scrapper_rescale_errors.txt', 'a') as file:
            print(f'{datetime.now()} : {msg}')
            file.write(f'{datetime.now()} : {msg}\n')

    else:
        with open('web_scrapper_rescale.txt', 'a') as file:
            print(f'{msg}')
            file.write(f'{msg}\n')


def web_crawl(queue, weblink, webcrawlResults):
    # we're logging the URL of the page fetched
    logging(f'{weblink}', 1)
    childrenLinks = []

    try:
        page = requests.get(weblink, timeout=10)
        soup = BeautifulSoup(page.content, "lxml")
        # a tag because we only need to find the hyperlinks
        for link in soup.find_all('a', href=True):
            child = link['href']
            # we only need to worry about absolute URLs that start with http/https
            if len(child) > 4:
                if child[0:4] == 'http':
                    # we're adding all the children with the absolute URLS. No duplicates
                    if child not in childrenLinks:
                        # we're getting and logging the URL found on the page
                        logging(f'\t{child}', 1)
                        childrenLinks.append(child)
        # we're adding all the child links to the parent URL
        if weblink not in webcrawlResults:
            webcrawlResults[weblink] = childrenLinks

        # we're iterating through the child links to see if we need to crawl through it
        for child in childrenLinks:
            if child not in webcrawlResults:
                queue.put(child)

    except requests.exceptions.RequestException as e:
        logging(f'error with {weblink}', 0)


def print_webcrawler_results(webcrawlResults):
    with open('website_crawled_results.txt', 'w') as file:
        for key in webcrawlResults:
            file.write(f'{key}\n')
            for value in webcrawlResults[key]:
                file.write(f'\t{value}\n')


def parallel(queue, webcrawlResults, totalCrawls):
    # only exit if the queue is empty or an arbitrary amount of web crawls
    currentCrawl = 0
    while not queue.empty() and not currentCrawl >= totalCrawls:
        count = 0
        for i in range(mp.cpu_count()):
            if currentCrawl >= totalCrawls:
                break
            currentCrawl += 1

            process_list = []
            if queue.empty():
                break
            else:
                url = queue.get()

            p = mp.Process(target=web_crawl, args=(queue, url, webcrawlResults,))
            p.start()
            process_list.append(p)

            for process in process_list:
                process.join()
            count += 1


def end_program():
    print('exiting')
    exit(0)


def main(url, totalCrawls):
    freeze_support()
    manager = mp.Manager()
    webcrawlResults = manager.dict()
    queue = manager.Queue()
    queue.put(url)
    try:
        parallel(queue, webcrawlResults, totalCrawls)
    except KeyboardInterrupt:
        end_program()
    print_webcrawler_results(webcrawlResults)
    print("exit")


if __name__ == '__main__':
    # we're getting the cmd line arguments and assigning the appropriate variables
    args = len(sys.argv)
    totalCrawls = -1

    match args:
        case 1:
            print('error: please enter an url')
            end_program()
        case 2:
            url = sys.argv[1]
        case 3:
            url = sys.argv[1]
            totalCrawls = int(sys.argv[2])
        case _:
            print('\n\nthis program will only be using the first two arguments\n\n')
            url = sys.argv[1]
            totalCrawls = int(sys.argv[2])
    main(url, totalCrawls)
