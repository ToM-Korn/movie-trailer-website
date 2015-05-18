# Favorite Movie Trailer Website #

## installation instructions ##
1. clone or copy this repository to your computer
2. go to the folder where you copied it
3. start it from command line with: python movies.py
4. follow the command promt

## Configuration instructions ##
if you'd like to have a new database you can delete the movies.db 
from the folder of installation

## Operating instructions ##
at the command promt you have several options

- input l for LIST all movies in db
- input d for DELETE one movie from db
- input q for QUIT and exit the programm
- input s for SHOW result - this generates a html stand alone website
	and displayes it to you in your webbrowser
	+ if you are not happy with the search result type 0 (zero) 
		to start a new search

## Files ##
- movies.py is the main file 
	it handles:
	+ user communication
	+ database administration
	+ search and data manipulation
- fresh_tomatoes.py (provided by Udacity)
	handles the generation of a stand alone website from
	a list of movie objects
	it is bootstrapped and therefore easy to change in apperance
- /docs/movies.html
	technical documentation

## copyright and licensing information ##
### Author of movies.py ###
ToM Krickl

### License ###
This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.

## contact information for the distributor or programmer ##
- email: git@krickl.eu
- phone: please ask me in mail 
- web: www.krickl.eu

## known bugs ##
currently non, please feel free to write me if you found one :) 

## troubleshooting ##
don't panic... write me a mail or solve the problem and commit it :)

## credits and acknowledgements ##
Thanks to Udacity for the fresh_tomatoes.py that generates the website.

Thanks to all python coders who generate and maintain those great libraries.

## changelog ##
please see the github repository commits