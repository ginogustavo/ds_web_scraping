## extract reviews from Yelp API

import io, time, json
import requests
from bs4 import BeautifulSoup

def retrieve_html(url):
    r = requests.get(url)
    return (r.status_code,r.text)

def parse_page(html):
    """
    Parse the reviews on a single page of a restaurant.

    Args:
        html (string): String of HTML corresponding to a Yelp restaurant

    Returns:
        tuple(list, string): a tuple of two elements
            first element: list of dictionaries corresponding to the extracted review information
            second element: URL for the next page of reviews (or None if it is the last page)
    """
    soup = BeautifulSoup(html,'html.parser')
    url_next = soup.find('link',rel='next')
    if url_next:
        url_next = url_next.get('href')
    else:
        url_next = None
    reviews = soup.find_all('div', itemprop="review")

    reviews_list = []
    # HINT: print reviews to see what http tag to extract
    for r in reviews:

        author = r.find('meta', itemprop='author').get("content")
        rating = r.find('meta', itemprop='ratingValue').get("content")
        rating = float(rating)
        date = r.find('meta', itemprop='datePublished').get("content")
        description = r.find('p', itemprop='description').getText()

        reviews_list.append({'author':author,'rating':rating, 'date':date, 'description':description})

    return reviews_list, url_next

def extract_reviews(url, html_fetcher):
    code, html = html_fetcher(url) # function implemented in Q0 should work
    rev_list, url_next = parse_page(html)

    globalList = rev_list
    while url_next:
        time.sleep(0.5)
        code, html = html_fetcher(url_next)
        rev_list, url_next = parse_page(html)
        globalList = globalList +  rev_list

    return globalList


data = extract_reviews('https://www.yelp.com/biz/the-jibarito-stop-chicago-2?start=220', html_fetcher=retrieve_html)
print(len(data))
# 40
print(data[0])
# {'author': 'Betsy F.', 'rating': '5.0', 'date': '2016-10-01', 'description': "Authentic, incredible ... " }
