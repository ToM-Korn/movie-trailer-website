import urllib
import json
import re
import os
import sqlite3
import sys
import fresh_tomatoes

omdb = "http://www.omdbapi.com/"
youtube = "https://www.youtube.com/"
imdb = "http://www.imdb.com/"

def search (url,dic_query,return_dict=False):
	search = urllib.urlopen(url+"?"+urllib.urlencode(dic_query))
	result = search.read()
	search.close()
	if return_dict:
		return dictify(result)
	else:
		return result

def dictify(jsonstr):
	return json.loads(jsonstr)

def user_com(DB):
	while 1:
		print 
		print ("USAGE: Enter q to quit, 0 for new search, s for show website")
		# print DB.get_list()
		search_input = raw_input("What movie do you like best? \n")
		if search_input == "q":
			break

		if search_input == "s":
			fresh_tomatoes.open_movies_page(DB.get_list())

		search_dict = {"s":search_input}
		result = search(omdb,search_dict,True)

		if "Search" in result:
			count = 1
			for elem in result["Search"]:
				print count, elem["Title"], elem["Year"], elem["Type"]
				count += 1

			movie_selected = raw_input("Which movie did you mean? Please enter the Index Number: ")
			if movie_selected == "0":
				pass
			else:
				dic_movie = get_movie(result["Search"][int(movie_selected)-1]["imdbID"])
				# try:
				# 	get_movie(result["Search"][int(movie_selected)-1]["imdbID"])
				# except:
				# 	print 
				# 	print "IMPORTANT: Please enter only one of the Numbers."
				DB.new_entry(dic_movie)
		else:
			print "Sorry no result. Please try again."

def get_movie(imdbID):
	search_string = {"i":imdbID,"plot":"short","tomatoes":"true"}
	result = search(omdb,search_string,True)

	yt_id = get_trailer(result["Title"]+" "+result["Year"])

	result["Trailer"] = yt_id
	result["imdbURL"] = imdb +'title/'+imdbID

	# print result["Trailer"]
	# print result["Title"]
	# print result["Plot"]
	# print result["Rated"]
	# print result["Poster"]
	# print result["tomatoRating"]
	# print result["imdbRating"]
	# print
	return result


def get_trailer(movie):
	search_text = movie+" trailer official"
	search_string = {"search_query":search_text}
	result = search(youtube+'results',search_string)

	# regex search : <div class="yt-lockup-content"><h3 class="yt-lockup-title"><a href="/watch?v=GWU-xLViib0" class="yt-uix-tile-link yt-ui-ellipsis yt-ui-ellipsis-2 yt-uix-sessionlink     spf-link " data-sessionlink="itct=CBoQ3DAYACITCLnY0v36v8UCFdCpHAodrjYA_ij0JFIsdGhlIGh1bmdlciBnYW1lcyAyMDEyIG1vdmllIHRyYWlsZXIgb2ZmaWNpYWw" title="The Hunger Games - Official Trailer (2012) HD Movie" aria-describedby="description-id-822575" rel="spf-prefetch" dir="ltr">The Hunger Games - Official Trailer (2012) HD Movie</a><span class="accessible-description" id="description-id-822575"> - Dauer: 2:55</span></h3><div class="yt-lockup-byline">von <a href="/user/THGfansite" class=" yt-uix-sessionlink     spf-link  g-hovercard" data-name="" data-sessionlink="itct=CBoQ3DAYACITCLnY0v36v8UCFdCpHAodrjYA_ij0JA" data-ytid="UC5kbrYM6LZHkcXm5jaRNgnA">THG Fansite</a></div><div class="yt-lockup-meta"><ul class="yt-lockup-meta-info"><li>vor 3 Jahren</li><li>444.396 Aufrufe</li></ul></div><div class="yt-lockup-description yt-ui-ellipsis yt-ui-ellipsis-2" dir="ltr"><b>The Hunger Games</b> - <b>Official Trailer</b> (<b>2012</b>) HD <b>Movie</b> Subscribe to <b>TRAILERS</b>: <a href="http://bit.ly/sxaw6h" target="_blank" title="http://bit.ly/sxaw6h" rel="nofollow" dir="ltr" class="yt-uix-redirect-link">http://bit.ly/sxaw6h</a> Subscribe to COMING SOON:&nbsp;...</div><div class="yt-lockup-badges"><ul class="yt-badge-list "><li class="yt-badge-item"><span class="yt-badge ">HD</span></li></ul> </div><div class="yt-lockup-action-menu yt-uix-menu-container"><div class="yt-uix-menu yt-uix-videoactionmenu hide-until-delayloaded" data-menu-content-id="yt-uix-videoactionmenu-menu" data-video-id="GWU-xLViib0">  <button class="yt-uix-button yt-uix-button-size-default yt-uix-button-action-menu yt-uix-button-empty yt-uix-button-has-icon no-icon-markup yt-uix-videoactionmenu-button yt-uix-menu-trigger yt-uix-tooltip" type="button" onclick=";return false;" aria-haspopup="true" aria-pressed="false" title="Mehr anzeigen" role="button" data-button-toggle="true"></button>
	# 	</div></div></div>

	match = re.search('\"yt-lockup-title\"\>\<a href=\"\/watch\?v\=([\w|\d|-|_]+)\"\s',result)
	if match:
		return match.group(1)
	else:
		return None

class db():
	def	__init__(self):
		create_db = True
		for l_file in os.listdir("./"):
			# print l_file
			if l_file == "movies.db":
				create_db = False

		self.con = sqlite3.connect("movies.db")
		self.c = self.con.cursor()
		# print create_db
		if create_db:
			self.c.execute('''CREATE TABLE movies
	         	(Title text, 
	         	Plot text, 
	         	Rated text, 
	         	Poster text,
	         	Trailer text, 
	         	tomatoRating text, 
	         	imdbRating text,
	         	imdbURL text)''')
			self.con.commit()

	def close(self):
		self.con.close()

	def new_entry(self,dic_movie):
		insert = (dic_movie["Title"],
			dic_movie["Plot"],
			dic_movie["Rated"],
			dic_movie["Poster"],
			dic_movie["Trailer"],
			dic_movie["tomatoRating"],
			dic_movie["imdbRating"],
			dic_movie["imdbURL"])
		self.c.execute('INSERT INTO movies VALUES (?,?,?,?,?,?,?,?)',insert)
		self.con.commit()

	def get_list(self):
		lst_movies = []
		result = self.c.execute('SELECT * FROM movies').fetchall()
		# print result
		for row in result:
			lst_movies.append(movie(row[0],row[1],row[2],row[3],row[4],row[5],row[6],row[7]))
		return lst_movies


class movie():
	def __init__(self,Title,Plot,Rated,Poster,Trailer,tomatoRating,imdbRating,imdbURL):
		self.title = Title
		self.plot = Plot
		self.rated = Rated
		self.poster = Poster
		self.trailer = Trailer
		self.tomatoRating = tomatoRating
		self.imdbRating = imdbRating
		self.imdbURL = imdbURL

if __name__ == "__main__":
	DB = db()
	user_com(DB)


# Plot In a dystopian future, the totalitarian nation of Panem is divided into 12 districts and the Capitol. Each year two young representatives from each district are selected by lot
# tery to participate in The Hunger Games. Part entertainment, part brutal retribution for a past rebellion, the televised games are broadcast throughout Panem. The 24 participants ar
# e forced to eliminate their competitors while the citizens of Panem are required to watch. When 16-year-old Katniss' young sister, Prim, is selected as District 12's female represen
# tative, Katniss volunteers to take her place. She and her male counterpart, Peeta, are pitted against bigger, stronger representatives, some of whom have trained for this their whol
# e lives.
# Rated PG-13
# tomatoImage certified
# Title The Hunger Games
# DVD 18 Aug 2012
# tomatoMeter 84
# Writer Gary Ross (screenplay), Suzanne Collins (screenplay), Billy Ray (screenplay), Suzanne Collins (novel)
# tomatoUserRating 4.1
# Production Lionsgate
# Actors Stanley Tucci, Wes Bentley, Jennifer Lawrence, Willow Shields
# tomatoFresh 232
# Type movie
# imdbVotes 609,997
# Website http://thehungergamesmovie.com
# tomatoConsensus Thrilling and superbly acted, The Hunger Games captures the dramatic violence, raw emotion, and ambitious scope of its source novel.
# Poster http://ia.media-imdb.com/images/M/MV5BMjA4NDg3NzYxMF5BMl5BanBnXkFtZTcwNTgyNzkyNw@@._V1_SX300.jpg
# tomatoRotten 44
# Director Gary Ross
# Released 23 Mar 2012
# tomatoUserReviews 896744
# Awards Nominated for 1 Golden Globe. Another 32 wins & 40 nominations.
# Genre Adventure, Sci-Fi
# tomatoUserMeter 81
# imdbRating 7.3
# Language English
# Country USA
# BoxOffice $408.0M
# Runtime 142 min
# tomatoReviews 276
# imdbID tt1392170
# Metascore 67
# Response True
# tomatoRating 7.2
# Year 2012