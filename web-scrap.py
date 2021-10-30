from bs4 import BeautifulSoup
import requests
import pandas as pd
import re

# define global parameters
URL = 'http://www.airlinequality.com/airline-reviews/airasia-x'
BASE_URL = 'http://www.airlinequality.com'
MASTER_LIST = []

def parse_review(review):
    """
    Parse important review meta data such as ratings, time of review, title, 
    etc.

    Parameters
    -------
    review - beautifulsoup tag 

    Return 
    -------
    outdf - pd.DataFrame
        DataFrame representation of parsed review
    """

    # get review header
    header = review.find('h2').text

    # get the numerical rating
    base_review = review.find('div', {'itemprop': 'reviewRating'})
    if base_review is None:
        rating = None
        rating_out_of = None
    else:
        rating = base_review.find('span', {'itemprop': 'ratingValue'}).text
        rating_out_of = base_review.find('span', {'itemprop': 'bestRating'}).text

    # get time of review
    time_of_review = review.find('h3').find('time')['datetime']

    # get whether review is verified
    if review.find('em'):
        verified = review.find('em').text
    else:
        verified = None

    # get actual text of review
    review_text = review.find('div', {'class': 'text_content'}).text

    outdf = pd.DataFrame({'header': header,
                         'rating': rating,
                         'rating_out_of': rating_out_of,
                         'time_of_review': time_of_review,
                         'verified': verified,
                         'review_text': review_text}, index=[0])

    return outdf

def return_next_page(soup):
    """
    return next_url if pagination continues else return None

    Parameters
    -------
    soup - BeautifulSoup object - required

    Return 
    -------
    next_url - str or None if no next page
    """
    next_url = None
    cur_page = soup.find('a', {'class': 'active'}, href=re.compile('airline-reviews/airasia'))
    cur_href = cur_page['href']
    # check if next page exists
    search_next = cur_page.findNext('li').get('class')
    if not search_next:
        next_page_href = cur_page.findNext('li').find('a')['href']
        next_url = BASE_URL + next_page_href
    return next_url

def create_soup_reviews(url):
    """
    iterate over each review, extract out content, and handle next page logic 
    through recursion

    Parameters
    -------
    url - str - required
        input url
    """
    # use global MASTER_LIST to extend list of all reviews 
    global MASTER_LIST
    soup = BeautifulSoup(requests.get(url).content, 'html.parser')
    reviews = soup.findAll('article', {'itemprop': 'review'})
    review_list = [parse_review(review) for review in reviews]
    MASTER_LIST.extend(review_list)
    next_url = return_next_page(soup)
    if next_url is not None:
        create_soup_reviews(next_url)


create_soup_reviews(URL)


finaldf = pd.concat(MASTER_LIST)
finaldf.shape # (339, 6)

finaldf.head(2)
finaldf.to_csv('products.csv', index=False, encoding='utf-8')
print(finaldf)
# header    rating  rating_out_of   review_text time_of_review  verified
#"if approved I will get my money back" 1   10  ✅ Trip Verified | Kuala Lumpur to Melbourne. ...    2018-08-07  Trip Verified
#   "a few minutes error"   3   10  ✅ Trip Verified | I've flied with AirAsia man...    2018-08-06  Trip Verified