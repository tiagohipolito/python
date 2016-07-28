# This is code for converting text file to Spotify playlists
# Make sure you have spotipy and requests and sys installed as modules in python
# Change the username, playlist name, and location of your data file below
# The txt file should be in the format of {track title}//{artist name}
	# don't include the brackets, just type the title and name
	# do include two forward slashes between the title and artists
		# if you want to separate your title and artist with something besides two forward slashes, change the variable "delim" below
		# be careful though to make sure you do not choose a character that might be present in the song or artist names (e.g. don't use ", ")
	# include an empty line at the end of your data file or the last artist won't be read correctly
	# the titles and artist names must not have typos

# You also will need to create and register an application with Spotify, but this is easy. Go to My Applications | Spotify Developer and create an app
	# Then, enter this url into the Redirect URLs section: "http://localhost:8888/callback"
	# Copy the client ID and secret into the variables named my_client_id and my_client_secret below

# When you first use this code and sign in to your account, a browser page will be opened that shows a blank page (or an error)
	# Copy the entire URL from this browser page and enter it into python

# Created in June 2016 by Michael Perrotta (michaelvperrotta@gmail.com) for personal use
# Python 2.7.11


import sys
import spotipy
import spotipy.util as util
import requests

######
##Change these:
username='tiago.hipolito'	#your username (not an email address)

createnewplaylist=True		## Set this to true to create a new playlist with the name below; set this to false to use an already created playlist, and follow instructions below
newplaylistname='Octane 2016'
## If using an already existing playlist, go to Spotify and right click on a playlist and select "Copy Spotify URI". Paste the value below, keeping only the numbers at the end of the URI
oldplaylistID='3uEcg6o2uf2ijoyeRj3zLiF'


dataFile = "/home/talves/Desktop/playlist.txt"
delim = "//"	#charecters between song title and artist in your data file; make sure this is not something that could be present in the song title or artist name

my_client_id='f57e112eeed041269bd0c31fda9c4d44'
my_client_secret='5cb21742b95b4dc0b023c9e71efa2440'
######
######


scope = 'user-library-read playlist-modify-public playlist-modify-private'

data = open(dataFile).readlines()

token = util.prompt_for_user_token(username, scope,client_id=my_client_id,client_secret=my_client_secret,redirect_uri='http://localhost:8888/callback')
myAuth="Bearer " + token

notfound=[]

if token:
	sp = spotipy.Spotify(auth=token)

	if createnewplaylist:
		r = sp.user_playlist_create(username, newplaylistname, False)
		playlistID=r['id']
	else:
		playlistID=oldplaylistID

	for line in data:
		l = line.split(delim)
		trackTitle=l[0]			## If you have any characters after your track title before your delimiter, add [:-1] (where 1 is equal to the number of additional characters)
		artist=l[1][:-2]		## [:-1] removes the newline at the end of every line. Make this [:-2] if you also have a space at the end of each line

		r = sp.search(trackTitle)

		found = False
		for track in r['tracks']['items']:
			if (track['artists'][0]['name'].lower()==artist.lower()):
				trackID = track['id']
				found = True
				break

		if not found:
			# print '****  Could not find song',trackTitle,'by artist',artist
			notfound.append(trackTitle+delim+artist)
		else:
			requests.post("https://api.spotify.com/v1/users/"+username+"/playlists/"+ playlistID +"/tracks?position=0&uris=spotify%3Atrack%3A"+trackID,headers={"Authorization":myAuth})
			print 'Added song',trackTitle,'by artist',artist

	print "\nSongs not added: "
	for line in notfound:
		print line
	print "\n"

else:
    print "Can't get token for", username
