import re
import pytz
import requests
import datetime
from bs4 import BeautifulSoup
from espncricinfo.exceptions import MatchNotFoundError, NoScorecardError
from espncricinfo.match import Match

bigbash_article_link = "http://www.espncricinfo.com/ci/content/series/1128817.html?template=fixtures"

r = requests.get(bigbash_article_link)
bigbash_article_html = r.text

soup = BeautifulSoup(bigbash_article_html, "html.parser")


bigbash1_items = soup.find_all("span",{"class": "fixture_date"})
bigbash_items = soup.find_all("span",{"class": "play_team"})
bigbash_article_dict = {}
date_dict = {}

# for div in bigbash_items:
# 	a = div.find('a')['href']
# 	bigbash_article_dict[div.find('a').string] = a
# 		#print(bigbash_article_dict)
i=0
s = {}
x = {}
date = []
match  = []
for div in bigbash1_items:
	i+=1
	if i %2 ==0:
		s = div.string.strip("\xa0local\n\r\t")
	elif i %2 !=0:
		x = div.string.strip("\xa0local\n\r\t")
	print(s)


	#print(bigbash_article_dict)

	#date_dict[div.find('span').string] = a
