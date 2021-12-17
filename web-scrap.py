from bs4 import BeautifulSoup
import requests
import pandas as pd
import re

# define global parameters
URL = 'https://www.exam4training.com/which-aws-service-delivers-data-videos-applications-and-apis-to-users-globally-with-low-latency-and-high-transfer-speeds'
MASTER_LIST = []

def parse_review(review):
    # get review header
    header = review.find('p').text

    # get actual text of review
    review_text = review.find('article', {'class': 'post'}).text

    outdf = pd.DataFrame({'header': header,
                         'review_text': review_text}, index=[0])

    return outdf

def return_next_page(soup):
    next_url = None
    cur_page = soup.find('div', {'class': 'content-area'})
    search_next = cur_page.findNext('div', {'class': 'nav-next'})

    if search_next:
      next_url = search_next.findNext('a')['href']
    return next_url

def create_soup_reviews(url):
    global MASTER_LIST
    req = requests.get(url, headers={"User-Agent": "Chrome"})
    soup = BeautifulSoup(req.content, 'html.parser')
    reviews = soup.findAll('div', {'class': 'content-area'})
    review_list = [parse_review(review) for review in reviews]
    print(MASTER_LIST)
    MASTER_LIST.extend(review_list)
    next_url = return_next_page(soup)
    finaldf = pd.concat(MASTER_LIST)
    finaldf.shape # (339, 6)
    finaldf.head(2)
    finaldf.to_csv('products2.csv', index=False, encoding='utf-8')
    if next_url is not None:
        create_soup_reviews(next_url)


create_soup_reviews(URL)


finaldf = pd.concat(MASTER_LIST)
finaldf.shape # (339, 6)

finaldf.head(2)
finaldf.to_csv('products.csv', index=False, encoding='utf-8')