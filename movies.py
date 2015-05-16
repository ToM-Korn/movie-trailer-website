# Command Line Tool for the Udacity Full Stack Web Developer Nano Degree
# This Requirement of the Project is to be able to understand Classes and Basic Python.
# I added a sqlite Database plus a CommandLine Tool to generate new Entries.
# Once entered a movie name the API of OMDBapi.com (open movie database) is called
# and the relslut is converted from json to a dict and stored in the Database including
# the first entry of trailor from youtube.
# 
# Once you are done collecting you videos you can hit the "s" key (for show) and
# a stand alone HTML Page will be generated with the content of the DB.
# Media Resources will be fetched from the web.
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

# Created by ToM Krickl 2015

# Import Modules
import urllib
import json
import re
import os
import sqlite3
import sys
import fresh_tomatoes

# Setup program wide variables
omdb = "http://www.omdbapi.com/"
youtube = "https://www.youtube.com/"
imdb = "http://www.imdb.com/"

def search (url,dic_query,return_dict=False):
	'''search (url,dic_query[,return_dict=False])
	url: the url to connect to e.g.: https://www.youtube.com/result
	dic_query: the GET parameters to be sent e.g.: s = what to search > {"s":"what to search"}
	return_dict: if the feedback from the website is a json you can get back a dict if you set this to true.

	With the given url and a query as a dict a GET request is sent,
	the data is fetched.
	if data is a json, set return_dict to True to receive a dict instead of just text.'''
	search = urllib.urlopen(url+"?"+urllib.urlencode(dic_query))
	result = search.read()
	search.close()
	if return_dict:
		return dictify(result)
	else:
		return result

def dictify(jsonstr):
	'''jsonstr: input a json str and get back a dict'''
	return json.loads(jsonstr)

def user_com(DB):
	'''main command line user communication. this schould be startet after the db is inizialised.

	the database must be given as object
	'''
	while 1:
		print ("\nUSAGE: \nq to quit, \ns for show website, \nl for list entries, \nd for deleting items \nin seach result 0 for new search\n")

		search_input = raw_input("What movie do you like best? \n")
		if search_input == "q":
			break

		elif search_input == "s":
			lst_movies = DB.get_list()
			movies = []
			for elem in lst_movies:
				movies.append(movie(elem))
			fresh_tomatoes.open_movies_page(movies)

		elif search_input == "l":
			print "Movies currently in DB"
			DB.print_list()
			
		elif search_input == "d":
			print "Movies currently in DB"
			DB.print_list()
			del_input = raw_input("Which one would you like to delete? 0 for none \n")
			if del_input != "0":
				try: 
					DB.delete_entry(int(del_input))
				except:
					print "\nIMPORTANT: Please enter only one of the ID's.\n"
		else:
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
					try:
						dic_movie = get_movie_data(result["Search"][int(movie_selected)-1]["imdbID"])
						DB.new_entry(dic_movie)
					except:
						print "\nIMPORTANT: Please enter only one of the Numbers.\n"
					
			else:
				print "Sorry no result. Please try again."
	return

def get_movie_data(imdbID):
	'''function to get data from the open movie database based on a given imdb id.

	returns a dict with a data to the movie including the youtube trailor and the imdb link.
	fields included are:
	Plot, Rated, tomatoImage, Title, DVD, tomatoMeter, Writer, tomatoUserRating, 
	Production, Actors, tomatoFresh, Type, imdbVotes, Website, tomatoConsensus, 
	Poster, tomatoRotten, Director, Released, tomatoUserReviews, Awards, Genre, 
	tomatoUserMeter, imdbRating, Language, Country, BoxOffice, Runtime, 
	tomatoReviews, imdbID, Metascore, Response, tomatoRating, Year,
	Trailer, imdbURL
	'''
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
	'''searches youtube for movie name plus "trailer official" and 
	returns the id of the first search result '''
	search_text = movie+" trailer official"
	search_string = {"search_query":search_text}
	result = search(youtube+'results',search_string)

	### part of youtube website we want to search for ###
	# regex search : <div class="yt-lockup-content"><h3 class="yt-lockup-title"><a href="/watch?v=GWU-xLViib0" class="yt-uix-tile-link yt-ui-ellipsis yt-ui-ellipsis-2 yt-uix-sessionlink     spf-link " data-sessionlink="itct=CBoQ3DAYACITCLnY0v36v8UCFdCpHAodrjYA_ij0JFIsdGhlIGh1bmdlciBnYW1lcyAyMDEyIG1vdmllIHRyYWlsZXIgb2ZmaWNpYWw" title="The Hunger Games - Official Trailer (2012) HD Movie" aria-describedby="description-id-822575" rel="spf-prefetch" dir="ltr">The Hunger Games - Official Trailer (2012) HD Movie</a><span class="accessible-description" id="description-id-822575"> - Dauer: 2:55</span></h3><div class="yt-lockup-byline">von <a href="/user/THGfansite" class=" yt-uix-sessionlink     spf-link  g-hovercard" data-name="" data-sessionlink="itct=CBoQ3DAYACITCLnY0v36v8UCFdCpHAodrjYA_ij0JA" data-ytid="UC5kbrYM6LZHkcXm5jaRNgnA">THG Fansite</a></div><div class="yt-lockup-meta"><ul class="yt-lockup-meta-info"><li>vor 3 Jahren</li><li>444.396 Aufrufe</li></ul></div><div class="yt-lockup-description yt-ui-ellipsis yt-ui-ellipsis-2" dir="ltr"><b>The Hunger Games</b> - <b>Official Trailer</b> (<b>2012</b>) HD <b>Movie</b> Subscribe to <b>TRAILERS</b>: <a href="http://bit.ly/sxaw6h" target="_blank" title="http://bit.ly/sxaw6h" rel="nofollow" dir="ltr" class="yt-uix-redirect-link">http://bit.ly/sxaw6h</a> Subscribe to COMING SOON:&nbsp;...</div><div class="yt-lockup-badges"><ul class="yt-badge-list "><li class="yt-badge-item"><span class="yt-badge ">HD</span></li></ul> </div><div class="yt-lockup-action-menu yt-uix-menu-container"><div class="yt-uix-menu yt-uix-videoactionmenu hide-until-delayloaded" data-menu-content-id="yt-uix-videoactionmenu-menu" data-video-id="GWU-xLViib0">  <button class="yt-uix-button yt-uix-button-size-default yt-uix-button-action-menu yt-uix-button-empty yt-uix-button-has-icon no-icon-markup yt-uix-videoactionmenu-button yt-uix-menu-trigger yt-uix-tooltip" type="button" onclick=";return false;" aria-haspopup="true" aria-pressed="false" title="Mehr anzeigen" role="button" data-button-toggle="true"></button>
	# 	</div></div></div>

	match = re.search('\"yt-lockup-title\"\>\<a href=\"\/watch\?v\=([\w|\d|-|_]+)\"\s',result)
	if match:
		return match.group(1)
	else:
		return None

class db():
	'''class for the database methods.
	on init a database file and table will be generated if it doesn't exist. 

	main methods are:
	new_entry(dic_movie) dic_movie should be generated from get_movie_data and 
		must include: Title, Plot, Rated, Poster, Trailer, tomatoRating, imdbRating, imdbURL
	get_list() returns a list of movie objects
	delete_entry() 
	close() closes the connection to the database

	'''
	def	__init__(self):
		create_db = True
		for l_file in os.listdir("./"):
			# print l_file
			if l_file == "movies.db":
				create_db = False

		self.con = sqlite3.connect("movies.db")
		self.c = self.con.cursor()
		self.nextid = 1
		# print create_db
		if create_db:
			self.c.execute('''CREATE TABLE movies
	         	(id INTEGER,
	         	Title text, 
	         	Plot text, 
	         	Rated text, 
	         	Poster text,
	         	Trailer text, 
	         	tomatoRating text, 
	         	imdbRating text,
	         	imdbURL text)''')
			self.con.commit()
		else:
			count = self.c.execute('SELECT * FROM movies').fetchall()
			self.nextid = count[-1][0]+1

	def close(self):
		self.con.close()

	def new_entry(self,dic_movie):
		insert = (self.nextid,
			dic_movie["Title"],
			dic_movie["Plot"],
			dic_movie["Rated"],
			dic_movie["Poster"],
			dic_movie["Trailer"],
			dic_movie["tomatoRating"],
			dic_movie["imdbRating"],
			dic_movie["imdbURL"])
		self.c.execute('INSERT INTO movies VALUES (?,?,?,?,?,?,?,?,?)',insert)
		self.con.commit()
		self.nextid += 1

	def print_list(self):
		list_entries = self.get_list()
		for elem in list_entries:
			print '#'+str(elem["id"])+" "+elem["Title"]

	def get_list(self):
		db_entries = self.get_entries()
		list_entries = []
		for elem in db_entries:
			dic_elem={}
			dic_elem["id"] = elem[0]
			dic_elem["Title"] = elem[1]
			dic_elem["Plot"] = elem[2]
			dic_elem["Rated"] = elem[3]
			dic_elem["Poster"] = elem[4]
			dic_elem["Trailer"] = elem[5]
			dic_elem["tomatoRating"] = elem[6]
			dic_elem["imdbRating"] = elem[7]
			dic_elem["imdbURL"] = elem[8]
			list_entries.append(dic_elem)
		return list_entries


	def get_entries(self):
		result = self.c.execute('SELECT * FROM movies').fetchall()
		# print result
		return result

	def delete_entry(self,movie_id):
		result = self.c.execute('DELETE FROM movies WHERE "id" = ?',str(movie_id))
		# print result
		return result

class movie():
	''' just creates an object of a movie '''
	def __init__(self,dict_movie):
		self.id = dict_movie["id"]
		self.title = dict_movie["Title"]
		self.plot = dict_movie["Plot"]
		self.rated = dict_movie["Rated"]
		self.poster = dict_movie["Poster"]
		self.trailer = dict_movie["Trailer"]
		self.tomatoRating = dict_movie["tomatoRating"]
		self.imdbRating = dict_movie["imdbRating"]
		self.imdbURL = dict_movie["imdbURL"]

	def __repr__(self):
		repr = "#"+str(self.id)+" "+self.Title
		return repr

if __name__ == "__main__":
	DB = db()
	user_com(DB)
	DB.close()

### Return example form the open movie database api ###

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




