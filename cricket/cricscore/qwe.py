import re
import pytz
import requests
import datetime
from flask import url_for
from bs4 import BeautifulSoup
from urllib.parse import urljoin
from espncricinfo.exceptions import MatchNotFoundError, NoScorecardError
from espncricinfo.match import Match

bigbash_article_link = "http://www.espncricinfo.com/ci/content/image/index.html?object=1128817"

r = requests.get(bigbash_article_link)
bigbash_article_html = r.text

soup = BeautifulSoup(bigbash_article_html, "html.parser")


bigbash_items = soup.find_all("div",{"class": "picture"})
bigbash_article_dict = {}


for div in bigbash_items:

	 a =[div.find('a')['href']]
	 print(a)
	 b = "http://www.espncricinfo.com"
	 c = urljoin(a,b)
	 #print(c)
	 c[bigbash_article_dict]
	 print(bigbash_article_dict)
