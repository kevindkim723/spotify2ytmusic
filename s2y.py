import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import spotipy.util as util
import json
import os
from ytmusicapi import YTMusic 




token=util.prompt_for_user_token(username="dodocannon", scope="user-library-read",client_id=os.environ.get("ci"), client_secret=os.environ.get("sd"),redirect_uri="https://localhost") #insert spotify API token here
sp = spotipy.Spotify(auth=token)


def get_playlist_tracks(username,playlist_id):
	#helper method to get the map of all spotify tracks within a limit (to fetch 100+ songs prohibited without the use of this method)
    results = sp.user_playlist_tracks(username,playlist_id)
    tracks = results['items']
    while results['next']:
        results = sp.next(results)
        tracks.extend(results['items'])
    return tracks
def getSpotifyTracks(username, playlist_id):
	#Parameters: Spotify username, Spotify playlist ID
	#Returns: String list of tracks in the playlist in format "SONG_NAME - ARTISTS"
	songs = []
	failed = []
	a = 0
	items = get_playlist_tracks(spotify_user, playlist_id)

	printProgressBar(0, len(items), prefix = 'Fetching songs...:', suffix = 'Complete',length=50)	
	for i in range(len(items)):
		try:
			artists = items[i]["track"]["artists"][0]["name"]
			for j in range(len(items[i]["track"]["artists"])-1):
				artists += ", " + items[i]["track"]["artists"][j+1]["name"]

			songs.append(items[i]["track"]["name"] + " - " + artists)
			printProgressBar(i+1, len(items), prefix = 'Fetching songs...:', suffix = 'Complete',length=50)	
			
		except Exception as e:
			failed.append(str(e) + " err on track no." + str(i))
		
		
	return songs,failed;

def createYTPlaylist(playlistname, description, listSongs):
	#Parameters: YTMusic playlist name, description, and the list of songs to be uploaded to the playlist
	#Returns: A YTMusic playlist with the designated name/description, with the list of songs in the playlist
	ytmusic = YTMusic('headers_auth.json')
	failed = []

	playlistID = ytmusic.create_playlist(playlistname, description)
	printProgressBar(0, len(listSongs), prefix = 'uploading songs...:', suffix = 'Complete', length=50)
	i=0
	for song in listSongs:
		try:
			printProgressBar(i+1, len(listSongs), prefix = 'uploading songs...:', suffix = 'Complete', length=50)
			search_results = ytmusic.search(song,"songs")
			ytmusic.add_playlist_items(playlistID, [search_results[0]['videoId']])
			i+=1

		except Exception as e:

			failed.append("failed on song: " + song + " from err. " + str(e))
	print("completed")


# Print iterations progress
#CITATION: https://stackoverflow.com/questions/3173320/text-progress-bar-in-the-console
def printProgressBar (iteration, total, prefix = '', suffix = '', decimals = 1, length = 100, fill = '█', printEnd = "\r"):
    """
    Call in a loop to create terminal progress bar
    @params:
        iteration   - Required  : current iteration (Int)
        total       - Required  : total iterations (Int)
        prefix      - Optional  : prefix string (Str)
        suffix      - Optional  : suffix string (Str)
        decimals    - Optional  : positive number of decimals in percent complete (Int)
        length      - Optional  : character length of bar (In)t
        fill        - Optional  : bar fill character (Str)
        printEnd    - Optional  : end character (e.g. "\r", "\r\n") (Str)
    """
    percent = ("{0:." + str(decimals) + "f}").format(100 * (iteration / float(total)))
    filledLength = int(length * iteration // total)
    bar = fill * filledLength + '-' * (length - filledLength)
    print(f'\r{prefix} |{bar}| {percent}% {suffix}', end = printEnd)
    # Print New Line on Complete
    if iteration == total: 
        print()

spotify_user="ENTER USER"
playlist_id = "ENTER ID"
playlist_id_full = "spotify:user:" + spotify_user + ":playlist:" + playlist_id

ytm_name = "r&b"
ytm_desc = "ty"


bundle = getSpotifyTracks(spotify_user, playlist_id)

songs = bundle[0]
spfails = bundle[1]

ytfails = createYTPlaylist(ytm_name, ytm_desc, songs)
for fail in spfails:
	print(fail)
for fail in ytfails:
	print(fail)



