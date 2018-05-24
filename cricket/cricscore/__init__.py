from flask import Flask
from flask import request
from flask import render_template
from flask_bootstrap import Bootstrap
from flask import redirect
from flask import url_for
from espncricinfo.match import Match
import collections
import datetime
import dateutil.parser
import pytz
import requests
import time
from bs4 import BeautifulSoup
from collections import OrderedDict
from apiclient.discovery import build
from requests.exceptions import ConnectionError



from score_constants import TEAM_DATA

from bigbashleaguepics import TEAM1_DATA
import pycricbuzz
import json

import pandas as pd

from urllib.parse import urljoin
from datetime import datetime

import praw

import collections
import datetime
import dateutil.parser
import pytz
import requests
import time




import re
try:
	import urllib.request as urllib2
except ImportError:
	import urllib2

# YouTube Developer Key
DEVELOPER_KEY = "AIzaSyC2wc6kpYSLyo5DMVcVeLq7hm2LRPBTnsk"
YOUTUBE_API_SERVICE_NAME = "youtube"
YOUTUBE_API_VERSION = "v3"

app = Flask(__name__)

# Time zone that determines when the next day occurs.
hawaii = pytz.timezone("Asia/Kolkata")

# Reddit API Key
reddit = praw.Reddit(client_id="HXHS4xHC8RqVgQ",
					 client_secret="Sfm6c88pE1O0CWpiTN8pPIHkGEs",
					 user_agent="bballfast by /u/microwavesam")


app = Flask(__name__)

bootstrap = Bootstrap(app)











@app.route("/")
def index1():
	datetime_today = datetime.datetime.now(hawaii)
	datestring_today = datetime_today.strftime("%m-%d-%Y")
	hot_Cricket_posts = get_hot_Cricket_post()
	batplayer_odi_ranking = get_batplayerodi_rankings()
	youtube_url = youtube_search("Cricbuzz", 2, True)
	youtube_url1 = youtube_search1("CricketCloud", 2, True)
	espn = esp()
	tabledata = get_points_tabledata()
	odi_ranking_table = get_odi_rankings()
	return render_template("index.html",title="THE WALL",
							hot_Cricket_posts = hot_Cricket_posts,
							youtube_url=youtube_url,
							youtube_url1=youtube_url1,
							gamest=get_games(),espn = espn,
							batplayer_odi_ranking = batplayer_odi_ranking,
							odi_ranking_table=odi_ranking_table,
								datestring_today=datestring_today)
@app.route("/sys_info.json")
def index():# you need an endpoint on the server that returns your info...
	 return get_games()

def get_points_tabledata():
	url = "http://www.espncricinfo.com/table/series/8044/big-bash-league"
	page = requests.get(url)
	soup = BeautifulSoup(page.text,"html.parser")

	teams_data = []
	for tr in soup.find_all("tr"):
		tds = tr.find_all("td")
		if len(tds) > 0:
			row = {'Teamname':tds[0].find("span",{"class": "team-names"}).text,'M': tds[1].text, 'W' : tds[2].text, 'L': tds[3].text,
																	  'T': tds[4].text ,'N/R':tds[5].text,'PT':tds[6].text,'NRR':tds[7].text,
																	  'FOR':tds[8].text,'AGAINST':tds[9].text}

			if (row["Teamname"] in TEAM1_DATA):
			   row["image"] = TEAM1_DATA[row["Teamname"]]["img"]
			   teams_data.append(row)


	#print (teams_data)



	return(teams_data)
def esp():
		abb = []
		m = Match('1122282')
		p = m.latest_batting
		p1=(p[1]['image_path'])
		p2= 'http://www.espncricinfo.com'
		p3=urljoin(p2,p1)
		abb.append(p3)
		#print(abb)
		return(abb)


def youtube_search(q, max_results=25, Cricbuzz=None):
	"""Searches YouTube for q and returns YouTube link.
	"""
	youtube = build(YOUTUBE_API_SERVICE_NAME, YOUTUBE_API_VERSION,
					developerKey=DEVELOPER_KEY)

	# Call the search.list method to retrieve results matching the specified
	# query term.
	if (Cricbuzz):
		search_response = youtube.search().list(q=q,
												part="id,snippet",
												maxResults=max_results,
												channelId="UCSRQXk5yErn4e14vN76upOw").execute()
	else:
		search_response = youtube.search().list(q=q,
												part="id,snippet",
												maxResults=max_results,
												type="video").execute()

	# Add each result to the appropriate list, and then display the lists of
	# matching videos, channels, and playlists.
	for search_result in search_response.get("items", []):
		if search_result["id"]["kind"] == "youtube#video":
			return "//www.youtube.com/embed/" + search_result["id"]["videoId"]

	return False

def youtube_search1(q, max_results=25, CricketCloud=None):
	"""Searches YouTube for q and returns YouTube link.
	"""
	youtube = build(YOUTUBE_API_SERVICE_NAME, YOUTUBE_API_VERSION,
					developerKey=DEVELOPER_KEY)

	# Call the search.list method to retrieve results matching the specified
	# query term.
	if (CricketCloud):
		search_response = youtube.search().list(q=q,
												part="id,snippet",
												maxResults=max_results,
												channelId="UC9l5bbc-S94CfORkfZXBQIg").execute()
	else:
		search_response = youtube.search().list(q=q,
												part="id,snippet",
												maxResults=max_results,
												type="video").execute()

	# Add each result to the appropriate list, and then display the lists of
	# matching videos, channels, and playlists.
	for search_result in search_response.get("items", []):
		if search_result["id"]["kind"] == "youtube#video":
			return "//www.youtube.com/embed/" + search_result["id"]["videoId"]

	return False




def get_cric_info_articles():

	cricinfo_article_link = "http://www.espncricinfo.com/ci/content/story/news.html"

	r = requests.get(cricinfo_article_link)
	cricinfo_article_html = r.text

	soup = BeautifulSoup(cricinfo_article_html, "html.parser")
	# print(soup.prettify())

	cric_info_items = soup.find_all("h2",{"class": "story-title"})
	cricinfo_article_dict = {}

	for div in cric_info_items:
		a = div.find('a')['href']
		b = 'http://www.espncricinfo.com/'
		c = urljoin(b,a)
		#print(c)
		cricinfo_article_dict[div.find('a').string] = c

	return cricinfo_article_dict


def get_cricbuzz_articles():

	cricbuzz_article_link = "http://www.cricbuzz.com/cricket-news"

	r = requests.get(cricbuzz_article_link)
	cricbuzz_article_html = r.text

	soup = BeautifulSoup(cricbuzz_article_html, "html.parser")
	# print(soup.prettify())

	cricbuzz_items = soup.find_all("h2",
									{"class": "cb-nws-hdln cb-font-18 line-ht24"})
	cricbuzz_article_dict = {}

	for div in cricbuzz_items:
		a = div.find('a')['href']
		b = 'http://www.cricbuzz.com'
		c = urljoin(b,a)
		cricbuzz_article_dict[div.find('a').string] = c

	return cricbuzz_article_dict




#def get_ndtvsports_articles():

	#ndtvsports_article_link = "https://sports.ndtv.com/cricket"

	#r = requests.get(ndtvsports_article_link)
	#ndtvsports_article_html = r.text

	#soup = BeautifulSoup(ndtvsports_article_html, "html.parser")
	# print(soup.prettify())

	#ndtvsports_items = soup.find_all("div",
									 #{"class": "post-title"})

	#ndtvsports_article_dict = {}

	#for div in ndtvsports_items:
		#ndtvsports_article_dict[div.find('a')['title']] = div.find('a')['href']

	#return ndtvsports_article_dict

def get_yahoonews_articles():

	yahoonews_article_link = "https://cricket.yahoo.net/news"

	r = requests.get(yahoonews_article_link)
	yahoonews_article_html = r.text

	soup = BeautifulSoup(yahoonews_article_html, "html.parser")
	# print(soup.prettify())

	cric_info_items = soup.find_all("h3",
									{"class": "title"})
	yahoonews_article_dict = {}

	for div in cric_info_items:
		a = div.find('a')['href']
		b = 'https://cricket.yahoo.net'
		c = urljoin(b,a)
		#print(c)
		yahoonews_article_dict[div.find('a').string] = c

	return yahoonews_article_dict

def get_bigbash_articles():

	bigbash_article_link = "https://www.bigbash.com.au/news"

	r = requests.get(bigbash_article_link)
	bigbash_article_html = r.text

	soup = BeautifulSoup(bigbash_article_html, "html.parser")
	# print(soup.prettify())

	bigbash_items = soup.find_all("div",
									{"class": "article-latest-news"})
	bigbash_article_dict = {}

	for div in bigbash_items:
		a = div.find('a')['href']
		b = 'https://www.bigbash.com.au'
		c = urljoin(b,a)
		#print(c)
		bigbash_article_dict[div.find('a').string] = c

	return bigbash_article_dict
def get_bcci_articles():

	bcci_article_link = "http://www.bcci.tv/news/2018/news"

	r = requests.get(bcci_article_link)
	bcci_article_html = r.text

	soup = BeautifulSoup(bcci_article_html, "html.parser")
	# print(soup.prettify())

	bcci_items = soup.find_all("div",
									{"class": "newsCol"})
	bcci_article_dict = {}

	for div in bcci_items:
		a = div.find('a')['href']
		b = 'https://www.bcci.tv'
		c = urljoin(b,a)
		#print(c)
		bcci_article_dict[div.find('p', {"class":"title"}).text] = c

	return bcci_article_dict

def get_games():
	c =pycricbuzz.Cricbuzz()
	matches = c.matches()
	gamest = []

	current_game1 = {}

	current_game10 = {}

	current_game11 = {}

	current_game12 = {}

	current_game13 = {}
	i=0
	scorecardid = 0
	commentaryid = 0

	#print(matches)

	for   match   in   matches:

	  scorecardid +=1
	  commentaryid +=1
	  #print(match)
	  try:
		  livescore1 =c.livescore(match[  'id'  ])
	  except TypeError:
		  livescore1 = None
	  #print(livescore1)
	  current_game1[    "status2"    ] = livescore1['matchinfo']['status']
	  current_game1[ 'progress2' ] = livescore1['matchinfo'][  'mchstate' ]
	  if  current_game1["progress2"] == "inprogress":
		  current_game1["live_img"] = TEAM_DATA[current_game1["progress2"]]["img"]
	  current_game1[ "teams2" ] = livescore1['matchinfo'][ 'mchdesc' ]
	  current_game1[ "series2" ] = livescore1['matchinfo'][ 'srs' ]
	  current_game1[ "matchno2" ] = livescore1['matchinfo'][ 'mnum' ]
	  current_game1[ "matchtype2" ] = livescore1['matchinfo'][  'type'  ]
	  current_game1[ "matchid2" ] = livescore1['matchinfo'][ 'id' ]
	  current_game1["scorecardid"] = int(scorecardid)
	  current_game1["commentaryid"] = int(commentaryid)



	  bat1=(livescore1.get('batting'))
	  if 'batting' in livescore1 :
		   bat2 = (bat1['batsman'])
		   current_game10 = {k+str(i): v for i, x in enumerate(bat2, 1) for k, v in x.items()}

		   #print(current_game10)



	  else:
		   print ('This does not have a text entry')


	  if 'batting' in livescore1 :
		   bat3 = (bat1['score'])
		   current_game12= {k+str(i): v for i, x in enumerate(bat3, 10) for k, v in x.items()}
	  else:
		   print ('This does not have a text entry')


	  bat4=(livescore1.get('batting'))
	  if 'batting' in livescore1 :
				bat10 = (bat4['team'])
				current_game1["Batting team"] =bat10
				if (current_game1["Batting team"] in TEAM_DATA):
				   current_game1["Batting_team_img"] = TEAM_DATA[current_game1["Batting team"]]["img"]
	  else:
		   print ('This does not have a text entry')

	  #if (bat10 in TEAM_DATA):
		  #current_game1["Batting_team_img"] = TEAM_DATA[bat10['img']]





	  bowl5=(livescore1.get('bowling'))
	  if 'bowling' in livescore1 :
		   bowl2 = (bowl5['bowler'])
		   current_game11= {k+str(i): v for i, x in enumerate(bowl2, 5) for k, v in x.items()}

		   #print(current_game11)


	  else:
		   print ('This does not have a text entry')


	  if 'bowling' in livescore1 :
		   bowl3 = (bowl5['score'])
		   current_game13= {k+str(i): v for i, x in enumerate(bowl3, 20) for k, v in x.items()}


	  else:
		   print ('This does not have a text entry')


	  bowl4=(livescore1.get('bowling'))
	  if 'bowling' in livescore1 :
			 bowl10 = (bowl4['team'])
			 current_game1["Bowling team"] =bowl10
			 if (current_game1["Bowling team"] in TEAM_DATA):
					 current_game1["Bowling_team_img"] = TEAM_DATA[current_game1["Bowling team"]]["img"]

	  else:

			 print ('This does not have a text entry')


	  #current_game =  dict(current_game1.items() + current_game10.items() + current_game11.items())
	  myDict = {}

	  i +=1
	  scr = "/Scorecard"+ str(i)
	  com = "/Commentary"+ str(i)

	  score = {'Scorecard1':scr}
	  comment = {'Commentary1':com}

	  myDict = {**current_game1, **current_game10, **current_game11, **current_game12, **current_game13, **score, **comment}
	  print(myDict)

	  #print(current_game1)

	  #for k,v in current_game1.items():
		  #myDict[k] = v

	  #for k,v in current_game10.items():
		  #myDict[k] = v

	  #for k,v in current_game11.items():
		  #myDict[k] = v

	  #print(myDict)
	  # def remove_dupes(a_list):
		# 		already_have = set()
		# 		new_table = []
		# 		for row in a_list:
		# 			row_hashable = tuple(sorted(row.items()))
		# 			if row_hashable not in already_have:
		# 				new_table.append(row)
		# 				already_have.add(row_hashable)
		# 		return new_table
	  # def uniqifier(seq):
		#     seen = set()
		#     seen_add = seen.add
		#     return (x for x in seq if not (x in seen or seen_add(x)))
	  #
	  # [dict(i) for i in uniqifier(tuple(i.items()) for i in myDict)]

	  #list(map(dict,OrderedDict.fromkeys(map(frozenset, map(dict.items, myDict)), None)))
	  # for k, v in enumerate([tuple(sorted(t.items())) for t in myDict]):
	  #    if v not in singlev:
	  #       singlev.append(myDict[k])
	  gamest.append((myDict))
	  print(gamest)





	  current_game1 = {}
	  current_game10 = {}
	  current_game11 = {}
	  current_game12 = {}
	  current_game13 = {}



	return gamest


def get_points_tabledata1():
	url = "http://www.espncricinfo.com/table/series/10886/season/2018/trans-tasman-t20-trophy"
	page = requests.get(url)
	soup = BeautifulSoup(page.text,"html.parser")
	trans = []
	teams_data = []
	for tr in soup.find_all("tr"):
		tds = tr.find_all("td")
		if len(tds) > 0:
			row = [{'Teamname':tds[0].find("span",{"class": "team-names"}).text,'M': tds[1].text, 'W' : tds[2].text, 'L': tds[3].text,
																	  'T': tds[4].text ,'N/R':tds[5].text,'PT':tds[6].text,'NRR':tds[7].text,
																	  'FOR':tds[8].text,'AGAINST':tds[9].text}]

			row.sort(key=lambda x: (x['PT'], x['NRR']), reverse=True)
			trans.append(row)
	return trans
	#print (teams_data)



def get_test_rankings():
	url = "http://www.espncricinfo.com/rankings/content/page/211271.html"
	page = requests.get(url)
	soup = BeautifulSoup(page.text,"html.parser")
	match_type = soup.find('h3').text
	#print(match_type)
	date_updated = soup.table.caption.text
	#print(date_updated)

	ret = []



	count = 0
	row = {}


	for tr in soup.find_all("tr"):
		count +=1
		tds = tr.find_all("td")
		if len(tds) > 0 :
			row = {'Team':tds[0].text,'Matches': tds[1].text, 'points' : tds[2].text, 'Rating': tds[3].text}
			if (row["Team"] in TEAM1_DATA):
			   row["image"] = TEAM1_DATA[row["Team"]]["img"]
			ret.append(row)
			row = {}
		if count == 11:
			   break
	row['match-type'] = match_type
	row['date-updated'] = date_updated
	ret.append(row)
	return(ret)








def get_odi_rankings():

	url = "http://www.espncricinfo.com/rankings/content/page/211271.html"
	page = requests.get(url)
	soup = BeautifulSoup(page.text,"html.parser")
	match_type = (soup.find_all('h3'))[1].text
	print(match_type)
	date_updated = (soup.find_all('caption'))[1].text
	print(date_updated)

	ret = []
	row = {}




	count = 0

	for tr in soup.find_all("tr"):
		count +=1
		if count >= 13:
			tds = tr.find_all("td")
			if len(tds) > 0 :
				row = {'Team':tds[0].text,'Matches': tds[1].text, 'points' : tds[2].text, 'Rating': tds[3].text}
				if (row["Team"] in TEAM1_DATA):
				   row["image"] = TEAM1_DATA[row["Team"]]["img"]
				ret.append(row)
				row = {}
				if count == 24:
				   break
	row['match-type'] = match_type
	row['date-updated'] = date_updated
	ret.append(row)
	return(ret)


def get_t20_rankings():
	url = "http://www.espncricinfo.com/rankings/content/page/211271.html"
	page = requests.get(url)
	soup = BeautifulSoup(page.text,"html.parser")
	match_type = (soup.find_all('h3'))[2].text
	print(match_type)
	date_updated = (soup.find_all('caption'))[2].text
	print(date_updated)

	ret = []
	row = {}



	count = 0

	for tr in soup.find_all("tr"):
		count +=1
		if count >= 25:
			tds = tr.find_all("td")
			if len(tds) > 0 :
				row = {'Team':tds[0].text,'Matches': tds[1].text, 'points' : tds[2].text, 'Rating': tds[3].text}
				if (row["Team"] in TEAM1_DATA):
				   row["image"] = TEAM1_DATA[row["Team"]]["img"]
				ret.append(row)

				row = {}
				if count == 42:
				   break
	row['match-type'] = match_type
	row['date-updated'] = date_updated
	ret.append(row)
	return(ret)


def get_women_rankings():
		url = "http://www.espncricinfo.com/rankings/content/page/211271.html"
		page = requests.get(url)
		soup = BeautifulSoup(page.text,"html.parser")
		match_type = (soup.find_all('h3'))[3].text
		print(match_type)
		date_updated = (soup.find_all('caption'))[3].text
		print(date_updated)

		ret = []
		row = {}



		count = 0

		for tr in soup.find_all("tr"):
			count +=1
			if count >= 44:
				tds = tr.find_all("td")
				if len(tds) > 0 :
					row = {'Team':tds[0].text,'Matches': tds[1].text, 'points' : tds[2].text, 'Rating': tds[3].text}
					if (row["Team"] in TEAM1_DATA):
					   row["image"] = TEAM1_DATA[row["Team"]]["img"]
					ret.append(row)
					row= {}
		row['match-type'] = match_type
		row['date-updated'] = date_updated
		ret.append(row)
		return(ret)

def get_batplayertest_rankings():
	res = requests.get("http://www.espncricinfo.com/rankings/content/page/211270.html")
	soup = BeautifulSoup(res.text,"lxml")
	 ## if any different table you expect to have then just change the index number
	 ## and the appropriate name in the selector
	item = soup.select("iframe[name='testbat']")[0]['src']
	req = requests.get(item)
	sauce = BeautifulSoup(req.text,"lxml")
	ret = []
	count = 0
	row = {}


	for tr in sauce.find_all('tr'):
		  count +=1
		  tds = tr.find_all('td')
		  if len(tds) > 0 :
				 row = {'Rank':tds[0].text,'Name': tds[1].text, 'country' : tds[2].text, 'Rating': tds[3].text}
				 if (row["Name"] in TEAM1_DATA):
				    row["image"] = TEAM1_DATA[row["Name"]]["img"]
				 ret.append(row)
				 row = {}
		  if count == 12:
			   break
	ret.append(row)
	return(ret)

def get_bowlplayertest_rankings():
	res = requests.get("http://www.espncricinfo.com/rankings/content/page/211270.html")
	soup = BeautifulSoup(res.text,"lxml")
	 ## if any different table you expect to have then just change the index number
	 ## and the appropriate name in the selector
	item = soup.select("iframe[name='testbat']")[1]['src']
	req = requests.get(item)
	sauce = BeautifulSoup(req.text,"lxml")
	ret = []
	count = 0
	row = {}


	for tr in sauce.find_all('tr'):
		  count +=1
		  tds = tr.find_all('td')
		  if len(tds) > 0 :
				 row = {'Rank':tds[0].text,'Name': tds[1].text, 'country' : tds[2].text, 'Rating': tds[3].text}
				 if (row["Name"] in TEAM1_DATA):
				     row["image"] = TEAM1_DATA[row["Name"]]["img"]
				 ret.append(row)
				 row = {}
		  if count == 12:
			   break
	ret.append(row)
	return(ret)

def get_allplayertest_rankings():
	res = requests.get("http://www.espncricinfo.com/rankings/content/page/211270.html")
	soup = BeautifulSoup(res.text,"lxml")
	 ## if any different table you expect to have then just change the index number
	 ## and the appropriate name in the selector
	item = soup.select("iframe[name='testbat']")[2]['src']
	req = requests.get(item)
	sauce = BeautifulSoup(req.text,"lxml")
	ret = []
	count = 0
	row = {}


	for tr in sauce.find_all('tr'):
		  count +=1
		  tds = tr.find_all('td')
		  if len(tds) > 0 :
				 row = {'Rank':tds[0].text,'Name': tds[1].text, 'country' : tds[2].text, 'Rating': tds[3].text}
				 if (row["Name"] in TEAM1_DATA):
				    row["image"] = TEAM1_DATA[row["Name"]]["img"]
				 ret.append(row)
				 row = {}
		  if count == 12:
			   break
	ret.append(row)
	return(ret)


def get_batplayerodi_rankings():
	res = requests.get("http://www.espncricinfo.com/rankings/content/page/211270.html")
	soup = BeautifulSoup(res.text,"lxml")
	 ## if any different table you expect to have then just change the index number
	 ## and the appropriate name in the selector
	item = soup.select("iframe[name='odibat']")[0]['src']
	req = requests.get(item)
	sauce = BeautifulSoup(req.text,"lxml")
	ret = []
	count = 0
	row = {}


	for tr in sauce.find_all('tr'):
		  count +=1
		  tds = tr.find_all('td')
		  if len(tds) > 0 :
				 row = {'Rank':tds[0].text,'Name': tds[1].text, 'country' : tds[2].text, 'Rating': tds[3].text}
				 if (row["Name"] in TEAM1_DATA):
				    row["image"] = TEAM1_DATA[row["Name"]]["img"]
				 ret.append(row)
				 row = {}
		  if count == 12:
			   break
	ret.append(row)
	return(ret)

def get_bowlplayerodi_rankings():
	res = requests.get("http://www.espncricinfo.com/rankings/content/page/211270.html")
	soup = BeautifulSoup(res.text,"lxml")
	 ## if any different table you expect to have then just change the index number
	 ## and the appropriate name in the selector
	item = soup.select("iframe[name='odibat']")[1]['src']
	req = requests.get(item)
	sauce = BeautifulSoup(req.text,"lxml")
	ret = []
	count = 0
	row = {}


	for tr in sauce.find_all('tr'):
		  count +=1
		  tds = tr.find_all('td')
		  if len(tds) > 0 :
				 row = {'Rank':tds[0].text,'Name': tds[1].text, 'country' : tds[2].text, 'Rating': tds[3].text}
				 if (row["Name"] in TEAM1_DATA):
				     row["image"] = TEAM1_DATA[row["Name"]]["img"]
				 ret.append(row)
				 row = {}
		  if count == 12:
			   break
	ret.append(row)
	return(ret)


def get_allplayerodi_rankings():
	res = requests.get("http://www.espncricinfo.com/rankings/content/page/211270.html")
	soup = BeautifulSoup(res.text,"lxml")
	 ## if any different table you expect to have then just change the index number
	 ## and the appropriate name in the selector
	item = soup.select("iframe[name='odibat']")[2]['src']
	req = requests.get(item)
	sauce = BeautifulSoup(req.text,"lxml")
	ret = []
	count = 0
	row = {}


	for tr in sauce.find_all('tr'):
		  count +=1
		  tds = tr.find_all('td')
		  if len(tds) > 0 :
				 row = {'Rank':tds[0].text,'Name': tds[1].text, 'country' : tds[2].text, 'Rating': tds[3].text}
				 if (row["Name"] in TEAM1_DATA):
				    row["image"] = TEAM1_DATA[row["Name"]]["img"]
				 ret.append(row)
				 row = {}
		  if count == 12:
			   break
	ret.append(row)
	return(ret)

def get_batplayet20_rankings():
	res = requests.get("http://www.espncricinfo.com/rankings/content/page/211270.html")
	soup = BeautifulSoup(res.text,"lxml")
	 ## if any different table you expect to have then just change the index number
	 ## and the appropriate name in the selector
	item = soup.select("iframe[name='t20bat']")[0]['src']
	req = requests.get(item)
	sauce = BeautifulSoup(req.text,"lxml")
	ret = []
	count = 0
	row = {}


	for tr in sauce.find_all('tr'):
		  count +=1
		  tds = tr.find_all('td')
		  if len(tds) > 0 :
				 row = {'Rank':tds[0].text,'Name': tds[1].text, 'country' : tds[2].text, 'Rating': tds[3].text}
				 if (row["Name"] in TEAM1_DATA):
				    row["image"] = TEAM1_DATA[row["Name"]]["img"]
				 ret.append(row)
				 row = {}
		  if count == 12:
			   break
	ret.append(row)
	return(ret)

def get_bowlplayet20_rankings():
	res = requests.get("http://www.espncricinfo.com/rankings/content/page/211270.html")
	soup = BeautifulSoup(res.text,"lxml")
	 ## if any different table you expect to have then just change the index number
	 ## and the appropriate name in the selector
	item = soup.select("iframe[name='t20bowl']")[0]['src']
	req = requests.get(item)
	sauce = BeautifulSoup(req.text,"lxml")
	ret = []
	count = 0
	row = {}


	for tr in sauce.find_all('tr'):
		  count +=1
		  tds = tr.find_all('td')
		  if len(tds) > 0 :
				 row = {'Rank':tds[0].text,'Name': tds[1].text, 'country' : tds[2].text, 'Rating': tds[3].text}
				 if (row["Name"] in TEAM1_DATA):
				    row["image"] = TEAM1_DATA[row["Name"]]["img"]
				 ret.append(row)
				 row = {}
		  if count == 12:
			   break
	ret.append(row)
	return(ret)


def get_allplayet20_rankings():
	res = requests.get("http://www.espncricinfo.com/rankings/content/page/211270.html")
	soup = BeautifulSoup(res.text,"lxml")
	 ## if any different table you expect to have then just change the index number
	 ## and the appropriate name in the selector
	item = soup.select("iframe[name='t20all']")[0]['src']
	req = requests.get(item)
	sauce = BeautifulSoup(req.text,"lxml")
	ret = []
	count = 0
	row = {}


	for tr in sauce.find_all('tr'):
		  count +=1
		  tds = tr.find_all('td')
		  if len(tds) > 0 :
				 row = {'Rank':tds[0].text,'Name': tds[1].text, 'country' : tds[2].text, 'Rating': tds[3].text}
				 if (row["Name"] in TEAM1_DATA):
				    row["image"] = TEAM1_DATA[row["Name"]]["img"]
				 ret.append(row)
				 row = {}
		  if count == 12:
			   break
	ret.append(row)
	return(ret)


def get_bat_womenplayerodi_rankings():
	res = requests.get("http://www.espncricinfo.com/rankings/content/page/211270.html")
	soup = BeautifulSoup(res.text,"lxml")
	 ## if any different table you expect to have then just change the index number
	 ## and the appropriate name in the selector
	item = soup.select("iframe[name='odibat']")[3]['src']
	req = requests.get(item)
	sauce = BeautifulSoup(req.text,"lxml")
	ret = []
	count = 0
	row = {}


	for tr in sauce.find_all('tr'):
		  count +=1
		  tds = tr.find_all('td')
		  if len(tds) > 0 :
				 row = {'Rank':tds[0].text,'Name': tds[1].text, 'country' : tds[2].text, 'Rating': tds[3].text}
				 if (row["Name"] in TEAM1_DATA):
				    row["image"] = TEAM1_DATA[row["Name"]]["img"]
				 ret.append(row)
				 row = {}
		  if count == 12:
			   break
	ret.append(row)
	return(ret)

def get_bowl_womenplayerodi_rankings():
	res = requests.get("http://www.espncricinfo.com/rankings/content/page/211270.html")
	soup = BeautifulSoup(res.text,"lxml")
	 ## if any different table you expect to have then just change the index number
	 ## and the appropriate name in the selector
	item = soup.select("iframe[name='odibat']")[4]['src']
	req = requests.get(item)
	sauce = BeautifulSoup(req.text,"lxml")
	ret = []
	count = 0
	row = {}


	for tr in sauce.find_all('tr'):
		  count +=1
		  tds = tr.find_all('td')
		  if len(tds) > 0 :
				 row = {'Rank':tds[0].text,'Name': tds[1].text, 'country' : tds[2].text, 'Rating': tds[3].text}
				 if (row["Name"] in TEAM1_DATA):
				    row["image"] = TEAM1_DATA[row["Name"]]["img"]
				 ret.append(row)
				 row = {}
		  if count == 12:
			   break
	ret.append(row)
	return(ret)

def get_all_womenplayerodi_rankings():
	res = requests.get("http://www.espncricinfo.com/rankings/content/page/211270.html")
	soup = BeautifulSoup(res.text,"lxml")
	 ## if any different table you expect to have then just change the index number
	 ## and the appropriate name in the selector
	item = soup.select("iframe[name='odibat']")[5]['src']
	req = requests.get(item)
	sauce = BeautifulSoup(req.text,"lxml")
	ret = []
	count = 0
	row = {}


	for tr in sauce.find_all('tr'):
		  count +=1
		  tds = tr.find_all('td')
		  if len(tds) > 0 :
				 row = {'Rank':tds[0].text,'Name': tds[1].text, 'country' : tds[2].text, 'Rating': tds[3].text}
				 if (row["Name"] in TEAM1_DATA):
				    row["image"] = TEAM1_DATA[row["Name"]]["img"]
				 ret.append(row)
				 row = {}
		  if count == 12:
			   break
	ret.append(row)
	return(ret)

def get_bat_womenplayert20_rankings():
	res = requests.get("http://www.espncricinfo.com/rankings/content/page/211270.html")
	soup = BeautifulSoup(res.text,"lxml")
	 ## if any different table you expect to have then just change the index number
	 ## and the appropriate name in the selector
	item = soup.select("iframe[name='odibat']")[6]['src']
	req = requests.get(item)
	sauce = BeautifulSoup(req.text,"lxml")
	ret = []
	count = 0
	row = {}


	for tr in sauce.find_all('tr'):
		  count +=1
		  tds = tr.find_all('td')
		  if len(tds) > 0 :
				 row = {'Rank':tds[0].text,'Name': tds[1].text, 'country' : tds[2].text, 'Rating': tds[3].text}
				 if (row["Name"] in TEAM1_DATA):
				    row["image"] = TEAM1_DATA[row["Name"]]["img"]
				 ret.append(row)
				 row = {}
		  if count == 12:
			   break
	ret.append(row)
	return(ret)

def get_bowl_womenplayert20_rankings():
	res = requests.get("http://www.espncricinfo.com/rankings/content/page/211270.html")
	soup = BeautifulSoup(res.text,"lxml")
	 ## if any different table you expect to have then just change the index number
	 ## and the appropriate name in the selector
	item = soup.select("iframe[name='odibat']")[7]['src']
	req = requests.get(item)
	sauce = BeautifulSoup(req.text,"lxml")
	ret = []
	count = 0
	row = {}


	for tr in sauce.find_all('tr'):
		  count +=1
		  tds = tr.find_all('td')
		  if len(tds) > 0 :
				 row = {'Rank':tds[0].text,'Name': tds[1].text, 'country' : tds[2].text, 'Rating': tds[3].text}
				 if (row["Name"] in TEAM1_DATA):
				     row["image"] = TEAM1_DATA[row["Name"]]["img"]
				 ret.append(row)
				 row = {}
		  if count == 12:
			   break
	ret.append(row)
	return(ret)

def get_all_womenplayert20_rankings():
	res = requests.get("http://www.espncricinfo.com/rankings/content/page/211270.html")
	soup = BeautifulSoup(res.text,"lxml")
	 ## if any different table you expect to have then just change the index number
	 ## and the appropriate name in the selector
	item = soup.select("iframe[name='odibat']")[8]['src']
	req = requests.get(item)
	sauce = BeautifulSoup(req.text,"lxml")
	ret = []
	count = 0
	row = {}


	for tr in sauce.find_all('tr'):
		  count +=1
		  tds = tr.find_all('td')
		  if len(tds) > 0 :
				 row = {'Rank':tds[0].text,'Name': tds[1].text, 'country' : tds[2].text, 'Rating': tds[3].text}
				 if (row["Name"] in TEAM1_DATA):
				    row["image"] = TEAM1_DATA[row["Name"]]["img"]
				 ret.append(row)
				 row = {}
		  if count == 12:
			   break
	ret.append(row)
	return(ret)



def get_hot_Cricket_post():
	"""Gets hottest /r/Cricket post from reddit.
	"""
	subreddit = reddit.subreddit("Cricket")
	submissions = []
	for submission in subreddit.top("day", limit=12):
		submissions.append(submission)

	return submissions
	"""
		if (submission):
			return (submission.permalink, submission.title)
		else:
			return ("http://www.redditstatus.com/", "Reddit Status?")
	"""









@app.route('/match', methods=["POST"])
def match_post_request():
	"""The score page after using the datepicker plugin.
	"""
	date1 = request.form["date"]
	datetimetoday = dateutil.parser.parse(date1)
	date = datetimetoday.strftime("%Y-%m-%d")
	#print(date)

	return render_match_page("match.html", date, date)



def render_match_page(page, datestring, title):
		datetime_today = dateutil.parser.parse(datestring)
		pretty_today = datetime_today.strftime("%Y %b, %d")
		datetime_yesterday = datetime_today - datetime.timedelta(1)
		datetime_tomorrow = datetime_today + datetime.timedelta(1)
		datestring_yesterday = datetime_yesterday.strftime("%Y-%m-%d")
		pretty_yesterday = datetime_yesterday.strftime("%Y %b, %d")
		datestring_tomorrow = datetime_tomorrow.strftime("%Y-%m-%d")
		pretty_tomorrow = datetime_tomorrow.strftime("%Y %b, %d")
		box = []
		#print(box)
		if (page == "match.html"):
			#print(datestring)
			def get_match_id(link):
					match_id = re.search(r'([0-9]{7})', link)
					if match_id is None:
						return None
					return match_id.group()

			url = "http://www.espncricinfo.com/ci/engine/match/index.html?date="+datestring
			print(url)



			r = requests.get(url)

			soup = BeautifulSoup(r.text, 'html.parser')


			spans = soup.findAll('span', {"class": "match-no"})


			matches_ids = []
			count= 0
			for s in spans:
				for a in s.findAll('a', href=lambda href: 'scorecard' in href):
					match_id = get_match_id(a['href'])
					if match_id is None:
						continue
					matches_ids.append(match_id)




			# ------parsing for matchno------
			for p in matches_ids:
				print(p)
				count+=1
				# where p is a match no, e.g p = '1122282'
				m = Match(p)
				#print(m)
				a={}
				a['matchid']=p
				a['status']=m.status
				a['description']=m.description
				a['series']=m.series
				a['date']=m.date
				a['match_title']=m.match_title
				a['result']=m.result
				a['ground_name']=m.ground_name
				box.append(a)
				a={}
		print(box)
		return render_template(page,
						   title=title,
						   date=datestring,
						   yesterday=datestring_yesterday,
						   tomorrow=datestring_tomorrow,
						   pretty_today=pretty_today,
						   pretty_yesterday=pretty_yesterday,
						   pretty_tomorrow=pretty_tomorrow,
						   box= box)


@app.route('/Summary/<matchid>')
def summary(matchid):
	"""Link for specific score pages for a certain day.
	"""

	# where p is a match no, e.g p = '1122282'
	p = matchid
	m = Match(p)
	print(m)
	box=[]
	a={}
	a['status']=m.status
	a['match_class']=m.match_class
	a['season']=m.season
	a['description']=m.description
	a['series']=m.series
	a['officials']=m.officials
	a['current_summary']=m.current_summary
	a['present_datetime_local']=m.present_datetime_local
	a['present_datetime_gmt']=m.present_datetime_gmt
	a['start_datetime_local ']=m.start_datetime_local
	a['start_datetime_gmt']=m.start_datetime_gmt
	a['cancelled_match']=m.cancelled_match
	a['rain_rule']=m.rain_rule
	a['date']=m.date
	a['town_area']=m.town_area
	a['town_name']=m.town_name
	a['town_id']=m.town_id
	a['weather_location_code']=m.weather_location_code
	a['match_title']=m.match_title
	a['result']=m.result
	a['ground_id']=m.ground_id
	a['ground_name']=m.ground_name
	a['lighting']=m.lighting
	a['followon']=m.followon
	a['scheduled_overs']=m.scheduled_overs
	a['innings_list']=m.innings_list
	a['innings']=m.innings
	a['latest_batting ']=m.latest_batting
	a['latest_bowling']=m.latest_bowling
	a['latest_innings']=m.latest_innings
	a['latest_innings_fow']=m.latest_innings_fow
	a['team_1']=m.team_1
	a['team_1_id ']=m.team_1_id
	a['team_1_abbreviation ']=m.team_1_abbreviation
	a['team_1_players']=m.team_1_players
	a['team_1_innings']=m.team_1_innings
	a['team_1_run_rate']=m.team_1_run_rate
	a['team_1_overs_batted']=m.team_1_overs_batted
	a['team_1_batting_result']=m.team_1_batting_result
	a['team_2']=m.team_2
	a['team_2_id ']=m.team_2_id
	a['team_2_abbreviation']=m.team_2_abbreviation
	a['team_2_players']=m.team_2_players
	a['team_2_innings']=m.team_2_innings
	a['team_2_run_rate']=m.team_2_run_rate
	a['team_2_overs_batted']=m.team_2_overs_batted
	a['team_2_batting_result']=m.team_2_batting_result
	a['home_team']=m.home_team
	a['batting_first']=m.batting_first
	a['match_winner']=m.match_winner
	a['toss_winner']=m.toss_winner
	a['toss_decision']=m.toss_decision
	box.append(a)
	a={}
	print(box)
	return render_template("Summary.html",
					   title="Summary",
					   box= box,
					   team=TEAM_DATA)


















@app.route('/Commentary/<commentaryid>')
def commentary1(commentaryid):
	c =pycricbuzz.Cricbuzz()
	matches = c.matches()
	commentary1 = []
	current_game3 = {}
	#print(commentaryid)
	count=0

	for   match   in   matches:
		if(match['mchstate'] != 'result'):
							  com1 = c.commentary(match['id'])
							  count +=1
							  if count ==1:
								  print(com1)
								  current_game3[    "status2"    ] = com1['matchinfo']['status']
								  current_game3[ 'progress2' ] = com1['matchinfo'][  'mchstate' ]
								  current_game3[ "teams2" ] = com1['matchinfo'][ 'mchdesc' ]
								  current_game3[ "matchno2" ] =com1['matchinfo'][ 'mnum' ]
								  current_game3[ "matchtype2" ] = com1['matchinfo'][  'type'  ]
								  current_game3[ "matchid2" ] = com1['matchinfo'][ 'id' ]
								  current_game3[ "matchseries" ] = com1['matchinfo'][ 'srs' ]
								  if 'commentary' in com1 :
									   for my_str in com1['commentary']:
										   current_game3[ "commentary2"] = my_str
										   if commentaryid =='1':
											   commentary1.append(current_game3)
											   current_game3 = {}

								  else:
										  print ('This does not have a text entry')
							  current_game3 = {}
							  if count ==2:
									  com1 = c.commentary(match['id'])
									  print(com1)
									  current_game3[    "status2"    ] = com1['matchinfo']['status']
									  current_game3[ 'progress2' ] = com1['matchinfo'][  'mchstate' ]
									  current_game3[ "teams2" ] = com1['matchinfo'][ 'mchdesc' ]
									  current_game3[ "matchno2" ] =com1['matchinfo'][ 'mnum' ]
									  current_game3[ "matchtype2" ] = com1['matchinfo'][  'type'  ]
									  current_game3[ "matchid2" ] = com1['matchinfo'][ 'id' ]
									  current_game3[ "matchseries" ] = com1['matchinfo'][ 'srs' ]
									  if 'commentary' in com1 :
										   for my_str in com1['commentary']:
											   current_game3[ "commentary2"] = my_str
											   if commentaryid =='2':
												   commentary1.append(current_game3)
												   current_game3 = {}

									  else:
											  print ('This does not have a text entry')
							  current_game3 = {}
							  if count ==3:
									  com1 = c.commentary(match['id'])
									  print(com1)
									  current_game3[    "status2"    ] = com1['matchinfo']['status']
									  current_game3[ 'progress2' ] = com1['matchinfo'][  'mchstate' ]
									  current_game3[ "teams2" ] = com1['matchinfo'][ 'mchdesc' ]
									  current_game3[ "matchno2" ] =com1['matchinfo'][ 'mnum' ]
									  current_game3[ "matchtype2" ] = com1['matchinfo'][  'type'  ]
									  current_game3[ "matchid2" ] = com1['matchinfo'][ 'id' ]
									  current_game3[ "matchseries" ] = com1['matchinfo'][ 'srs' ]
									  if 'commentary' in com1 :
										   for my_str in com1['commentary']:
											   current_game3[ "commentary2"] = my_str
											   if commentaryid =='3':
												   commentary1.append(current_game3)
												   current_game3 = {}

									  else:
											  print ('This does not have a text entry')
							  current_game3 = {}
							  if count ==4:
									  com1 = c.commentary(match['id'])
									  print(com1)
									  current_game3[    "status2"    ] = com1['matchinfo']['status']
									  current_game3[ 'progress2' ] = com1['matchinfo'][  'mchstate' ]
									  current_game3[ "teams2" ] = com1['matchinfo'][ 'mchdesc' ]
									  current_game3[ "matchno2" ] =com1['matchinfo'][ 'mnum' ]
									  current_game3[ "matchtype2" ] = com1['matchinfo'][  'type'  ]
									  current_game3[ "matchid2" ] = com1['matchinfo'][ 'id' ]
									  current_game3[ "matchseries" ] = com1['matchinfo'][ 'srs' ]
									  if 'commentary' in com1 :
										   for my_str in com1['commentary']:
											   current_game3[ "commentary2"] = my_str
											   if commentaryid =='4':
												   commentary1.append(current_game3)
												   current_game3 = {}

									  else:
											  print ('This does not have a text entry')
							  current_game3 = {}
							  if count ==5:
									  com1 = c.commentary(match['id'])
									  print(com1)
									  current_game3[    "status2"    ] = com1['matchinfo']['status']
									  current_game3[ 'progress2' ] = com1['matchinfo'][  'mchstate' ]
									  current_game3[ "teams2" ] = com1['matchinfo'][ 'mchdesc' ]
									  current_game3[ "matchno2" ] =com1['matchinfo'][ 'mnum' ]
									  current_game3[ "matchtype2" ] = com1['matchinfo'][  'type'  ]
									  current_game3[ "matchid2" ] = com1['matchinfo'][ 'id' ]
									  current_game3[ "matchseries" ] = com1['matchinfo'][ 'srs' ]
									  if 'commentary' in com1 :
										   for my_str in com1['commentary']:
											   current_game3[ "commentary2"] = my_str
											   if commentaryid =='5':
												   commentary1.append(current_game3)
												   current_game3 = {}

									  else:
											  print ('This does not have a text entry')
							  current_game3 = {}
				 #print(commentary1)
	return render_template("Commentary.html",
						   title="Commentary",
						   commentary1=commentary1,
						   team=TEAM_DATA)
@app.route("/sys_info.json")
def index2(): # you need an endpoint on the server that returns your info...
	 return  commentary1(commentaryid)


@app.route('/Scorecard/<scorecardid>')
def scorecard(scorecardid):
	c =pycricbuzz.Cricbuzz()
	matches = c.matches()
	scoreecard = []
	scoreecard1 = {}
	scoreecard2 = {}
	scoreecard3 = {}
	scoreecard4 = {}
	scoreecard5 = {}
	current_game4 = {}
	current_game10 = {}
	current_game11 = {}
	current_game21 = {}
	current_game31 = {}
	count=0



	for   match   in   matches:
		 count+=1
		 if(match['mchstate'] != 'preview'):
		  if count ==1:
				 sod1 = c.scorecard(match['id'])
				 current_game4[    "status4"    ] = sod1['matchinfo']['status']
				 current_game4[ 'progress4' ] = sod1['matchinfo'][  'mchstate' ]
				 current_game4[ "teams4" ] = sod1['matchinfo'][ 'mchdesc' ]
				 current_game4[ "matchno4" ] =sod1['matchinfo'][ 'mnum' ]
				 current_game4[ "matchtype4" ] = sod1['matchinfo'][  'type'  ]
				 current_game4[ "matchid4" ] = sod1['matchinfo'][ 'id' ]
				 current_game4[ "series4" ] = sod1['matchinfo'][ 'srs' ]
				 if 'scorecard' in sod1 :

				   current_game4[ "2nd-innings-overs"] = sod1['scorecard'][0]['overs']
				   current_game4[ "2nd-innings-runrate"] = sod1['scorecard'][0]['runrate']
				   current_game4[ "2nd-innings-runs"] = sod1['scorecard'][0]['runs']
				   current_game4[ "2nd-innings-batteam"] = sod1['scorecard'][0]['batteam']
				   current_game4[ "2nd-innings-bowlteam"] = sod1['scorecard'][0]['bowlteam']
				   current_game4[ "2nd-innings-wickets"] = sod1['scorecard'][0]['wickets']
				   current_game4[ "2nd-innings-inningsdesc"] = sod1['scorecard'][0]['inngdesc']

				   try:
					   current_game4[ "1st-innings-overs"] = sod1['scorecard'][1]['overs']
					   current_game4[ "1st-innings-runrate"] = sod1['scorecard'][1]['runrate']
					   current_game4[ "1st-innings-runs"] = sod1['scorecard'][1]['runs']
					   current_game4[ "1st-innings-batteam"] = sod1['scorecard'][1]['batteam']
					   current_game4[ "1st-innings-bowlteam"] = sod1['scorecard'][1]['bowlteam']
					   current_game4[ "1st-innings-wickets"] = sod1['scorecard'][1]['wickets']
					   current_game4[ "1st-innings-inningsdesc"] = sod1['scorecard'][1]['inngdesc']
				   except IndexError:
					   current_game4[ "1st-innings-overs"] = current_game4[ "1st-innings-runrate"]=current_game4[ "1st-innings-runs"] =current_game4[ "1st-innings-batteam"]=current_game4[ "1st-innings-bowlteam"] =current_game4[ "1st-innings-wickets"] =current_game4[ "1st-innings-inningsdesc"]=None
				 else:
					  print ('This does not have a text entry')
				 if 'squad' in sod1 :
					 current_game4[ "squad1-team" ] = sod1['squad'][0]['team']
					 current_game4[ "squad2-team" ] = sod1['squad'][1][ 'team' ]
					 current_game4[ "squad1-members" ] = sod1['squad'][0]['members']
					 current_game4[ "squad2-members" ] = sod1['squad'][1]['members']
				 else:
					  print ('This does not have a text entry')


				 if 'scorecard' in sod1 :
					 sod2 = sod1['scorecard'][0]['bowlcard']
					 current_game10 = {k+str(i): v for i, x in enumerate(sod2, 10) for k, v in x.items()}
				 else:
					 print ('This does not have a text entry')
				 if 'scorecard' in sod1 :
					 sod3 = sod1['scorecard'][0]['batcard']
					 print(sod3)
					 current_game11 = {k+str(i): v for i, x in enumerate(sod3, 30) for k, v in x.items()}
					 print(current_game11)
				 else:
					 print ('This does not have a text entry')
				 if 'scorecard' in sod1 :
					 try:
						 sod4 = sod1['scorecard'][1]['bowlcard']
						 current_game21 = {k+str(i): v for i, x in enumerate(sod4, 50) for k, v in x.items()}
					 except IndexError:
						 sod4 = None
				 else:
					 print ('This does not have a text entry')
				 if 'scorecard' in sod1 :
					 try:
						 sod5 = sod1['scorecard'][1]['batcard']
						 current_game31 = {k+str(i): v for i, x in enumerate(sod5, 70) for k, v in x.items()}
					 except IndexError:
						 sod4 = None
				 else:
					 print ('This does not have a text entry')


				 scoreecard1 = {**current_game4, **current_game10, **current_game11, **current_game21, **current_game31}
				 if scorecardid =='1':
					 scoreecard.append(scoreecard1)
				 else:
					 continue

				 current_game4 = {}
				 current_game10 = {}
				 current_game11 = {}
				 current_game21 = {}
				 current_game31 = {}
		  if count ==2:

				 sod1 = c.scorecard(match['id'])
				 current_game4[    "status4"    ] = sod1['matchinfo']['status']
				 current_game4[ 'progress4' ] = sod1['matchinfo'][  'mchstate' ]
				 current_game4[ "teams4" ] = sod1['matchinfo'][ 'mchdesc' ]
				 current_game4[ "matchno4" ] =sod1['matchinfo'][ 'mnum' ]
				 current_game4[ "matchtype4" ] = sod1['matchinfo'][  'type'  ]
				 current_game4[ "matchid4" ] = sod1['matchinfo'][ 'id' ]
				 current_game4[ "series4" ] = sod1['matchinfo'][ 'srs' ]
				 if 'scorecard' in sod1 :

				   current_game4[ "2nd-innings-overs"] = sod1['scorecard'][0]['overs']
				   current_game4[ "2nd-innings-runrate"] = sod1['scorecard'][0]['runrate']
				   current_game4[ "2nd-innings-runs"] = sod1['scorecard'][0]['runs']
				   current_game4[ "2nd-innings-batteam"] = sod1['scorecard'][0]['batteam']
				   current_game4[ "2nd-innings-bowlteam"] = sod1['scorecard'][0]['bowlteam']
				   current_game4[ "2nd-innings-wickets"] = sod1['scorecard'][0]['wickets']
				   current_game4[ "2nd-innings-inningsdesc"] = sod1['scorecard'][0]['inngdesc']
				   try:
					   current_game4[ "1st-innings-overs"] = sod1['scorecard'][1]['overs']
					   current_game4[ "1st-innings-runrate"] = sod1['scorecard'][1]['runrate']
					   current_game4[ "1st-innings-runs"] = sod1['scorecard'][1]['runs']
					   current_game4[ "1st-innings-batteam"] = sod1['scorecard'][1]['batteam']
					   current_game4[ "1st-innings-bowlteam"] = sod1['scorecard'][1]['bowlteam']
					   current_game4[ "1st-innings-wickets"] = sod1['scorecard'][1]['wickets']
					   current_game4[ "1st-innings-inningsdesc"] = sod1['scorecard'][1]['inngdesc']
				   except IndexError:
					   current_game4[ "1st-innings-overs"] = current_game4[ "1st-innings-runrate"]=current_game4[ "1st-innings-runs"] =current_game4[ "1st-innings-batteam"]=current_game4[ "1st-innings-bowlteam"] =current_game4[ "1st-innings-wickets"] =current_game4[ "1st-innings-inningsdesc"]=None
				 else:
					  print ('This does not have a text entry')
				 if 'squad' in sod1 :
					 current_game4[ "squad1-team" ] = sod1['squad'][0]['team']
					 current_game4[ "squad2-team" ] = sod1['squad'][1][ 'team' ]
					 current_game4[ "squad1-members" ] = sod1['squad'][0]['members']
					 current_game4[ "squad2-members" ] = sod1['squad'][1]['members']
				 else:
					  print ('This does not have a text entry')


				 if 'scorecard' in sod1 :
					 sod2 = sod1['scorecard'][0]['bowlcard']
					 current_game10 = {k+str(i): v for i, x in enumerate(sod2, 10) for k, v in x.items()}
				 else:
					 print ('This does not have a text entry')
				 if 'scorecard' in sod1 :
					 sod3 = sod1['scorecard'][0]['batcard']
					 current_game11 = {k+str(i): v for i, x in enumerate(sod3, 30) for k, v in x.items()}
				 else:
					 print ('This does not have a text entry')
				 if 'scorecard' in sod1 :
					 try:
						 sod4 = sod1['scorecard'][1]['bowlcard']
						 current_game21 = {k+str(i): v for i, x in enumerate(sod4, 50) for k, v in x.items()}
					 except IndexError:
						 sod4 = None
				 else:
					 print ('This does not have a text entry')
				 if 'scorecard' in sod1 :
					 try:
						 sod5 = sod1['scorecard'][1]['batcard']
						 current_game31 = {k+str(i): v for i, x in enumerate(sod5, 70) for k, v in x.items()}
					 except IndexError:
						 sod4 = None
				 else:
					 print ('This does not have a text entry')


				 scoreecard2= {**current_game4, **current_game10, **current_game11, **current_game21, **current_game31}
				 print(scorecardid)
				 if scorecardid =='2':
					 scoreecard.append(scoreecard2)
					 #print(scoreecard)
				 # print(scoreecard2)
				 # print(scorecardid)
				 # scoreecard.append(scoreecard2)
				 # print(scoreecard)
				 current_game4 = {}
				 current_game10 = {}
				 current_game11 = {}
				 current_game21 = {}
				 current_game31 = {}




		  if count ==3:
				 sod1 = c.scorecard(match['id'])
				 current_game4[    "status4"    ] = sod1['matchinfo']['status']
				 current_game4[ 'progress4' ] = sod1['matchinfo'][  'mchstate' ]
				 current_game4[ "teams4" ] = sod1['matchinfo'][ 'mchdesc' ]
				 current_game4[ "matchno4" ] =sod1['matchinfo'][ 'mnum' ]
				 current_game4[ "matchtype4" ] = sod1['matchinfo'][  'type'  ]
				 current_game4[ "matchid4" ] = sod1['matchinfo'][ 'id' ]
				 current_game4[ "series4" ] = sod1['matchinfo'][ 'srs' ]
				 if 'scorecard' in sod1 :

				   current_game4[ "2nd-innings-overs"] = sod1['scorecard'][0]['overs']
				   current_game4[ "2nd-innings-runrate"] = sod1['scorecard'][0]['runrate']
				   current_game4[ "2nd-innings-runs"] = sod1['scorecard'][0]['runs']
				   current_game4[ "2nd-innings-batteam"] = sod1['scorecard'][0]['batteam']
				   current_game4[ "2nd-innings-bowlteam"] = sod1['scorecard'][0]['bowlteam']
				   current_game4[ "2nd-innings-wickets"] = sod1['scorecard'][0]['wickets']
				   current_game4[ "2nd-innings-inningsdesc"] = sod1['scorecard'][0]['inngdesc']
				   try:
					   current_game4[ "1st-innings-overs"] = sod1['scorecard'][1]['overs']
					   current_game4[ "1st-innings-runrate"] = sod1['scorecard'][1]['runrate']
					   current_game4[ "1st-innings-runs"] = sod1['scorecard'][1]['runs']
					   current_game4[ "1st-innings-batteam"] = sod1['scorecard'][1]['batteam']
					   current_game4[ "1st-innings-bowlteam"] = sod1['scorecard'][1]['bowlteam']
					   current_game4[ "1st-innings-wickets"] = sod1['scorecard'][1]['wickets']
					   current_game4[ "1st-innings-inningsdesc"] = sod1['scorecard'][1]['inngdesc']
				   except IndexError:
					   current_game4[ "1st-innings-overs"] = current_game4[ "1st-innings-runrate"]=current_game4[ "1st-innings-runs"] =current_game4[ "1st-innings-batteam"]=current_game4[ "1st-innings-bowlteam"] =current_game4[ "1st-innings-wickets"] =current_game4[ "1st-innings-inningsdesc"]=None
				 else:
					  print ('This does not have a text entry')
				 if 'squad' in sod1 :
					 current_game4[ "squad1-team" ] = sod1['squad'][0]['team']
					 current_game4[ "squad2-team" ] = sod1['squad'][1][ 'team' ]
					 current_game4[ "squad1-members" ] = sod1['squad'][0]['members']
					 current_game4[ "squad2-members" ] = sod1['squad'][1]['members']
				 else:
					  print ('This does not have a text entry')


				 if 'scorecard' in sod1 :
					 sod2 = sod1['scorecard'][0]['bowlcard']
					 current_game10 = {k+str(i): v for i, x in enumerate(sod2, 10) for k, v in x.items()}
				 else:
					 print ('This does not have a text entry')
				 if 'scorecard' in sod1 :
					 sod3 = sod1['scorecard'][0]['batcard']
					 current_game11 = {k+str(i): v for i, x in enumerate(sod3, 30) for k, v in x.items()}
				 else:
					 print ('This does not have a text entry')
				 if 'scorecard' in sod1 :
					 try:
						 sod4 = sod1['scorecard'][1]['bowlcard']
						 current_game21 = {k+str(i): v for i, x in enumerate(sod4, 50) for k, v in x.items()}
					 except IndexError:
						 sod4 = None
				 else:
					 print ('This does not have a text entry')
				 if 'scorecard' in sod1 :
					 try:
						 sod5 = sod1['scorecard'][1]['batcard']
						 current_game31 = {k+str(i): v for i, x in enumerate(sod5, 70) for k, v in x.items()}
					 except IndexError:
						 sod4 = None
				 else:
					 print ('This does not have a text entry')


				 scoreecard3 = {**current_game4, **current_game10, **current_game11, **current_game21, **current_game31}
				 if scorecardid =='3':
					 scoreecard.append(scoreecard3)
					 #print(scoreecard)
				 current_game4 = {}
				 current_game10 = {}
				 current_game11 = {}
				 current_game21 = {}
				 current_game31 = {}


		  if count ==4:
				 sod1 = c.scorecard(match['id'])
				 current_game4[    "status4"    ] = sod1['matchinfo']['status']
				 current_game4[ 'progress4' ] = sod1['matchinfo'][  'mchstate' ]
				 current_game4[ "teams4" ] = sod1['matchinfo'][ 'mchdesc' ]
				 current_game4[ "matchno4" ] =sod1['matchinfo'][ 'mnum' ]
				 current_game4[ "matchtype4" ] = sod1['matchinfo'][  'type'  ]
				 current_game4[ "matchid4" ] = sod1['matchinfo'][ 'id' ]
				 current_game4[ "series4" ] = sod1['matchinfo'][ 'srs' ]
				 if 'scorecard' in sod1 :
				   current_game4[ "2nd-innings-overs"] = sod1['scorecard'][0]['overs']
				   current_game4[ "2nd-innings-runrate"] = sod1['scorecard'][0]['runrate']
				   current_game4[ "2nd-innings-runs"] = sod1['scorecard'][0]['runs']
				   current_game4[ "2nd-innings-batteam"] = sod1['scorecard'][0]['batteam']
				   current_game4[ "2nd-innings-bowlteam"] = sod1['scorecard'][0]['bowlteam']
				   current_game4[ "2nd-innings-wickets"] = sod1['scorecard'][0]['wickets']
				   current_game4[ "2nd-innings-inningsdesc"] = sod1['scorecard'][0]['inngdesc']
				   try:
					   current_game4[ "1st-innings-overs"] = sod1['scorecard'][1]['overs']
					   current_game4[ "1st-innings-runrate"] = sod1['scorecard'][1]['runrate']
					   current_game4[ "1st-innings-runs"] = sod1['scorecard'][1]['runs']
					   current_game4[ "1st-innings-batteam"] = sod1['scorecard'][1]['batteam']
					   current_game4[ "1st-innings-bowlteam"] = sod1['scorecard'][1]['bowlteam']
					   current_game4[ "1st-innings-wickets"] = sod1['scorecard'][1]['wickets']
					   current_game4[ "1st-innings-inningsdesc"] = sod1['scorecard'][1]['inngdesc']
				   except IndexError:
					   current_game4[ "1st-innings-overs"] = current_game4[ "1st-innings-runrate"]=current_game4[ "1st-innings-runs"] =current_game4[ "1st-innings-batteam"]=current_game4[ "1st-innings-bowlteam"] =current_game4[ "1st-innings-wickets"] =current_game4[ "1st-innings-inningsdesc"]=None
				 else:
					  print ('This does not have a text entry')
				 if 'squad' in sod1 :
					 current_game4[ "squad1-team" ] = sod1['squad'][0]['team']
					 current_game4[ "squad2-team" ] = sod1['squad'][1][ 'team' ]
					 current_game4[ "squad1-members" ] = sod1['squad'][0]['members']
					 current_game4[ "squad2-members" ] = sod1['squad'][1]['members']
				 else:
					  print ('This does not have a text entry')


				 if 'scorecard' in sod1 :
					 sod2 = sod1['scorecard'][0]['bowlcard']
					 current_game10 = {k+str(i): v for i, x in enumerate(sod2, 10) for k, v in x.items()}
				 else:
					 print ('This does not have a text entry')
				 if 'scorecard' in sod1 :
					 sod3 = sod1['scorecard'][0]['batcard']
					 current_game11 = {k+str(i): v for i, x in enumerate(sod3, 30) for k, v in x.items()}
				 else:
					 print ('This does not have a text entry')
				 if 'scorecard' in sod1 :
					 try:
						 sod4 = sod1['scorecard'][1]['bowlcard']
						 current_game21 = {k+str(i): v for i, x in enumerate(sod4, 50) for k, v in x.items()}
					 except IndexError:
						 sod4 = None
				 else:
					 print ('This does not have a text entry')
				 if 'scorecard' in sod1 :
					 try:
						 sod5 = sod1['scorecard'][1]['batcard']
						 current_game31 = {k+str(i): v for i, x in enumerate(sod5, 70) for k, v in x.items()}
					 except IndexError:
						 sod4 = None
				 else:
					 print ('This does not have a text entry')

				 scoreecard4 = {**current_game4, **current_game10, **current_game11, **current_game21, **current_game31}
				 if scorecardid =='4':
					 scoreecard.append(scoreecard4)
				 current_game4 = {}
				 current_game10 = {}
				 current_game11 = {}
				 current_game21 = {}
				 current_game31 = {}




		  if  count ==5:
				 sod1 = c.scorecard(match['id'])
				 current_game4[    "status4"    ] = sod1['matchinfo']['status']
				 current_game4[ 'progress4' ] = sod1['matchinfo'][  'mchstate' ]
				 current_game4[ "teams4" ] = sod1['matchinfo'][ 'mchdesc' ]
				 current_game4[ "matchno4" ] =sod1['matchinfo'][ 'mnum' ]
				 current_game4[ "matchtype4" ] = sod1['matchinfo'][  'type'  ]
				 current_game4[ "matchid4" ] = sod1['matchinfo'][ 'id' ]
				 current_game4[ "series4" ] = sod1['matchinfo'][ 'srs' ]
				 if 'scorecard' in sod1 :
				   current_game4[ "2nd-innings-overs"] = sod1['scorecard'][0]['overs']
				   current_game4[ "2nd-innings-runrate"] = sod1['scorecard'][0]['runrate']
				   current_game4[ "2nd-innings-runs"] = sod1['scorecard'][0]['runs']
				   current_game4[ "2nd-innings-batteam"] = sod1['scorecard'][0]['batteam']
				   current_game4[ "2nd-innings-bowlteam"] = sod1['scorecard'][0]['bowlteam']
				   current_game4[ "2nd-innings-wickets"] = sod1['scorecard'][0]['wickets']
				   current_game4[ "2nd-innings-inningsdesc"] = sod1['scorecard'][0]['inngdesc']
				   try:
					   current_game4[ "1st-innings-overs"] = sod1['scorecard'][1]['overs']
					   current_game4[ "1st-innings-runrate"] = sod1['scorecard'][1]['runrate']
					   current_game4[ "1st-innings-runs"] = sod1['scorecard'][1]['runs']
					   current_game4[ "1st-innings-batteam"] = sod1['scorecard'][1]['batteam']
					   current_game4[ "1st-innings-bowlteam"] = sod1['scorecard'][1]['bowlteam']
					   current_game4[ "1st-innings-wickets"] = sod1['scorecard'][1]['wickets']
					   current_game4[ "1st-innings-inningsdesc"] = sod1['scorecard'][1]['inngdesc']
				   except IndexError:
					   current_game4[ "1st-innings-overs"] = current_game4[ "1st-innings-runrate"]=current_game4[ "1st-innings-runs"] =current_game4[ "1st-innings-batteam"]=current_game4[ "1st-innings-bowlteam"] =current_game4[ "1st-innings-wickets"] =current_game4[ "1st-innings-inningsdesc"]=None
				 else:
					  print ('This does not have a text entry')
				 if 'squad' in sod1 :
					 current_game4[ "squad1-team" ] = sod1['squad'][0]['team']
					 current_game4[ "squad2-team" ] = sod1['squad'][1][ 'team' ]
					 current_game4[ "squad1-members" ] = sod1['squad'][0]['members']
					 current_game4[ "squad2-members" ] = sod1['squad'][1]['members']
				 else:
					  print ('This does not have a text entry')


				 if 'scorecard' in sod1 :
					 sod2 = sod1['scorecard'][0]['bowlcard']
					 current_game10 = {k+str(i): v for i, x in enumerate(sod2, 10) for k, v in x.items()}
				 else:
					 print ('This does not have a text entry')
				 if 'scorecard' in sod1 :
					 sod3 = sod1['scorecard'][0]['batcard']
					 current_game11 = {k+str(i): v for i, x in enumerate(sod3, 30) for k, v in x.items()}
				 else:
					 print ('This does not have a text entry')
				 if 'scorecard' in sod1 :
					 try:
						 sod4 = sod1['scorecard'][1]['bowlcard']
						 current_game21 = {k+str(i): v for i, x in enumerate(sod4, 50) for k, v in x.items()}
					 except IndexError:
						 sod4 = None
				 else:
					 print ('This does not have a text entry')
				 if 'scorecard' in sod1 :
					 try:
						 sod5 = sod1['scorecard'][1]['batcard']
						 current_game31 = {k+str(i): v for i, x in enumerate(sod5, 70) for k, v in x.items()}
					 except IndexError:
						 sod4 = None
				 else:
					 print ('This does not have a text entry')
				 myDict = {}
				 scoreecard5 = {**current_game4, **current_game10, **current_game11, **current_game21, **current_game31}
				 if scorecardid =='5':
					 scoreecard.append(scoreecard5)


				 current_game4 = {}
				 current_game10 = {}
				 current_game11 = {}
				 current_game21 = {}
				 current_game31 = {}
	print(scoreecard)
	return render_template("Scorecard.html",
						   title="Scorecard",
						   scoreecard=scoreecard,
						   team=TEAM_DATA)
@app.route("/sys_info.json")
def index3(): # you need an endpoint on the server that returns your info...
	 return  scorecard(scorecardid)


@app.route('/Rankings')
def rankings():
	"""Default Highlights page.
	"""
	batplayer_odi_ranking = get_batplayerodi_rankings()
	batplayer_test_ranking = get_batplayertest_rankings()
	a=[]
	tabledata = get_points_tabledata()
	a.append(tabledata)
	test_ranking_table = get_test_rankings()
	a.append(test_ranking_table)
	odi_ranking_table = get_odi_rankings()
	a.append(odi_ranking_table)
	t20_ranking_table = get_t20_rankings()
	a.append(t20_ranking_table)
	women_ranking_table = get_women_rankings()
	a.append(women_ranking_table)
	print(a)

	return render_template("Rankings.html",
						   batplayer_odi_ranking = batplayer_odi_ranking,
						   batplayer_test_ranking = batplayer_test_ranking,
						   test_ranking_table = test_ranking_table,
						   odi_ranking_table = odi_ranking_table,
						   t20_ranking_table = t20_ranking_table,
						   women_ranking_table = women_ranking_table,
						   title="Rankings",
						   team=TEAM_DATA)


@app.route('/playersratting')
def rankings1():
	# batplayer_test_ranking = get_batplayertest_rankings()
	# bowlplayer_test_ranking = get_bowlplayertest_rankings()
	# allplayer_test_ranking = get_allplayertest_rankings()
	batplayer_odi_ranking = get_batplayerodi_rankings()
	bowlplayer_odi_ranking = get_bowlplayerodi_rankings()
	allplayer_odi_ranking = get_allplayerodi_rankings()
	batplayer_t20_ranking = get_batplayet20_rankings()
	bowlplayer_t20_ranking = get_bowlplayet20_rankings()
	allplayer_t20_ranking = get_allplayet20_rankings()
	wombatplayer_odi_ranking = get_bat_womenplayerodi_rankings()
	wombowlplayer_odi_ranking = get_bowl_womenplayerodi_rankings()
	womallplayer_odi_ranking = get_all_womenplayerodi_rankings()
	womabatplayer_t20_ranking = get_bat_womenplayert20_rankings()
	womaballplayer_t20_ranking = get_bowl_womenplayert20_rankings()
	womallplayer_t20_ranking = get_all_womenplayert20_rankings()
	return render_template("playersratting.html",
						   # batplayer_test_ranking = batplayer_test_ranking,
						   # bowlplayer_test_ranking = bowlplayer_test_ranking,
						   # allplayer_test_ranking = allplayer_test_ranking,
						   batplayer_odi_ranking = batplayer_odi_ranking,
						   bowlplayer_odi_ranking = bowlplayer_odi_ranking,
						   allplayer_odi_ranking = allplayer_odi_ranking,
						   batplayer_t20_ranking = batplayer_t20_ranking,
						   bowlplayer_t20_ranking = bowlplayer_t20_ranking,
						   allplayer_t20_ranking = allplayer_t20_ranking,
						   wombatplayer_odi_ranking = wombatplayer_odi_ranking,
						   wombowlplayer_odi_ranking = wombowlplayer_odi_ranking,
						   womallplayer_odi_ranking = womallplayer_odi_ranking,
						   womabatplayer_t20_ranking = womabatplayer_t20_ranking,
						   womaballplayer_t20_ranking = womaballplayer_t20_ranking,
						   womallplayer_t20_ranking = womallplayer_t20_ranking,
						   title="playersratting",
						   team=TEAM_DATA)

@app.route('/womensratting')
def rankings2():
	women_ranking_table =  get_women_rankings()
	wombatplayer_odi_ranking = get_bat_womenplayerodi_rankings()
	wombowlplayer_odi_ranking = get_bowl_womenplayerodi_rankings()
	womallplayer_odi_ranking = get_all_womenplayerodi_rankings()
	womabatplayer_t20_ranking = get_bat_womenplayert20_rankings()
	womaballplayer_t20_ranking = get_bowl_womenplayert20_rankings()
	womallplayer_t20_ranking = get_all_womenplayert20_rankings()
	return render_template("womensratting.html",
						   women_ranking_table = women_ranking_table,
						   wombatplayer_odi_ranking = wombatplayer_odi_ranking,
						   wombowlplayer_odi_ranking = wombowlplayer_odi_ranking,
						   womallplayer_odi_ranking = womallplayer_odi_ranking,
						   womabatplayer_t20_ranking = womabatplayer_t20_ranking,
						   womaballplayer_t20_ranking = womaballplayer_t20_ranking,
						   womallplayer_t20_ranking = womallplayer_t20_ranking,
						   title="womensranking",
						   team=TEAM_DATA)











@app.route('/Points-Table')
def PointsTable():
	"""Default Full commentary page.@app.route('/Scorecard')

	"""

	url = "http://www.espncricinfo.com/table/series/10886/season/2018/trans-tasman-t20-trophy"
	page = requests.get(url)
	soup = BeautifulSoup(page.text,"html.parser")
	trans = []
	teams_data = []
	for tr in soup.find_all("tr"):
		tds = tr.find_all("td")
		if len(tds) > 0:
			row = {'Teamname':tds[0].find("span",{"class": "team-names"}).text,'M': tds[1].text, 'W' : tds[2].text, 'L': tds[3].text,
																	  'T': tds[4].text ,'N/R':tds[5].text,'PT':tds[6].text,'NRR':tds[7].text,
																	  'FOR':tds[8].text,'AGAINST':tds[9].text}
			if (row["Teamname"] in TEAM1_DATA):
			   row["image"] = TEAM1_DATA[row["Teamname"]]["img"]
			#row.sort(key=lambda x: (x['PT'], x['NRR']), reverse=True)
			trans.append(row)
			#print(trans)

	url = "http://www.espncricinfo.com/table/series/8043/season/2017/sheffield-shield/"
	page = requests.get(url)
	soup = BeautifulSoup(page.text,"html.parser")
	trans1 = []
	teams_data = []
	for tr in soup.find_all("tr"):
		tds = tr.find_all("td")
		if len(tds) > 0:
			row = {'Teamname':tds[0].find("span",{"class": "team-names"}).text,'M': tds[1].text, 'W' : tds[2].text, 'L': tds[3].text,
																	  'T': tds[4].text ,'D':tds[5].text,'N/R':tds[6].text,'PT':tds[7].text
																	  }
			if (row["Teamname"] in TEAM1_DATA):
			   row["image"] = TEAM1_DATA[row["Teamname"]]["img"]
			#row.sort(key=lambda x: (x['PT'], x['NRR']), reverse=True)
			trans1.append(row)
			#print(trans1)
	url = "http://www.espncricinfo.com/table/series/8679/pakistan-sl"
	page = requests.get(url)
	soup = BeautifulSoup(page.text,"html.parser")
	trans2 = []
	teams_data = []
	row = {}
	for tr in soup.find_all("tr"):
		tds = tr.find_all("td")
		if len(tds) > 0:
			row = {'Teamname':tds[0].find("span",{"class": "team-names"}).text,'M': tds[1].text, 'W' : tds[2].text, 'L': tds[3].text,
																	  'T': tds[4].text ,'N/R':tds[5].text,'PT':tds[6].text,'NRR':tds[7].text,
																	  'FOR':tds[8].text,'AGAINST':tds[9].text }
			if (row["Teamname"] in TEAM1_DATA):
			   row["image"] = TEAM1_DATA[row["Teamname"]]["img"]


			#row.sort(key=lambda x: (x['PT'], x['NRR']), reverse=True)
			trans2.append(row)
			print(trans2)


	return render_template("Points-Table.html",
						   title="Points-Table",
						   pointstt = trans,
						   pointstt1 = trans1,
						   pointstt2 = trans2,


						   team=teams_data)
@app.route('/Blogs')
def get_reddif_blogpost():
		url = "http://www.rediff.com/cricket/blogs"
		page = requests.get(url)
		soup = BeautifulSoup(page.text,"html.parser")
		reddif_info_items = soup.find_all("div",{"class": "ingap"})
		reddif_info_dict = {}
		teams_data = []
		for div in reddif_info_items:
				a = div.find('a')['href']
				reddif_info_dict[div.find('a').text] = a


		return render_template("Blogs.html",
						   title="Blogs",
						   reddif_info_dict = reddif_info_dict,
						   team=TEAM_DATA)

@app.route('/News')
def news():
	"""Default news page.
	"""
	yahoonews_posts = get_yahoonews_articles()
	cricbuzz_posts = get_cricbuzz_articles()
	cricinfo_posts = get_cric_info_articles()
	return render_template("News.html",
	cricinfo_posts = cricinfo_posts,
							cricbuzz_posts = cricbuzz_posts,
							yahoonews_posts = yahoonews_posts,
						   title="News",
						   team=TEAM_DATA)
@app.route('/Photos')
def photos():
	"""Default photos page.
	"""
	return render_template("Photos.html",
						   title="Photos",
						   team=TEAM_DATA)









































@app.route('/channel/<username>')
def channel(username):


	return render_template('username.html', username=username)





@app.errorhandler(404)
def page_not_found(e):
	return render_template("404.html"), 404








if __name__=="__main__":
	app.run(host="0.0.0.0", port=3030, threaded=True, debug=True)


url_for('channel', username='cricketschedule',_external=True)
