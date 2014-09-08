from urlparse import urlparse, parse_qs
import re
from django.shortcuts import redirect
'''
needs the following functions:
	- convert gifsound URL to GFYsound URL
		x- parse GifSound URL
			x- extract gif URL from gifsound URL
	- send gif URL, receive JSON of new GfysoundURL
'''

def grab_gif_url(url):
	'''Grabs a url from gifsound.com and returns 
	the gif location in it'''
	data = urlparse(url)
	gif_url = data.gif
	if gif_url:
		return gif_url
	else:
		raise AttributeError('gif URL not found')


def grab_convert_url(url):
	'''takes gifsound URL, grabs gif and converts/returns a gfy link'''
	gif_url = grab_gif_url(url)
	newurl = "http://upload.gfycat.com/transcode?fetchUrl=" + gif_url
	return newurl

def grab_youtube_url(url):
    '''Grabs a url from gifsound.com and returns
    the youtube url in it'''
    data = urlparse(url)
    query_data = parse_qs(data.query)
    if query_data['sound']:
        if query_data['start']:
        	return "%s%s" % (query_data['sound'], query_data['start'])
        else:
        	return "%s" % query_data['sound']
    else:
    	raise AttributeError('video URL not found')



