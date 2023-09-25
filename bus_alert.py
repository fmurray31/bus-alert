import requests
import time
import smtplib
from bs4 import BeautifulSoup

#TODO
# send email
# refine search for bus route, eg " 39a", ",39a", etc, also allow multiple routes

URL = "https://www.dublinbus.ie/news"

# 30 minutes in seconds
WAIT_TIME = 1800

BUS_ROUTE = "39a"

sending_email = ""
receiving_email = ""


previous_url = ""
new_url = ""

# variable to track errors in the program, after the first error any future error will
# kill the program
error_sent = False

# function to handle errors. On first error sends message, on second ends the program
def error_encountered(error):   
    if not error_sent:
        print(error)
        error_sent = True
    else:
        exit

# searches the text at a given post for mentions of the requested bus route
def text_search(post_url):
    post_response = requests.get(post_url)
    
    if post_response.status_code == 200:
        post_soup = BeautifulSoup(post_response.text, 'html.parser')
        post_text = post_soup.find('div', class_='wysiwyg').get_text(strip=True)
        if BUS_ROUTE in post_text:
            send_email(BUS_ROUTE, post_url)

def send_email(route, url):
    print(route + " found")
    print(url)

# main block
while True:
    response = requests.get(URL)
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')

        news_posts_links = []

        news_posts = soup.find_all('a', 'news-card')
        for post in news_posts:
            news_posts_links.append(post['href'])

        post_urls = []

        for post_link in news_posts_links:
            post_link = post_link.replace('news/', '')
            post_urls.append(URL + post_link)

        new_url = post_urls[0]

        for post_url in post_urls:
            if (post_url == previous_url): break
            text_search(post_url)

        previous_url = new_url

    else:
        error_encountered("failed to reach website, status code: " + response.status_code)

    time.sleep(WAIT_TIME)