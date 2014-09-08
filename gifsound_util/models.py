from django.db import models
from django.core.validators import RegexValidator
from urlparse import urlparse, parse_qs
import pafy
import urllib2
import json
import re


class Gifsound(models.Model):
    gifsound_url = models.URLField(
        blank=False,
        validators=[
            RegexValidator(
                regex='^https?:\/\/([a-zA-Z\d-]+\.){0,}gifsound\.com',
                message="Enter a valid gifsound.com URL.",
                code='invalid_gifsound_url'
            ),
        ]
    )
    '''
    needs the following functions:
    - convert gifsound URL to GFYsound URL
    x- parse GifSound URL
    x- extract gif URL from gifsound URL
    - send gif URL, receive JSON of new GfysoundURL
    '''

    def get_gif_url(self):
        '''Grabs a url from gifsound.com and returns
        the gif location in it'''
        regex = re.compile(r'(https?://\S+)')
        data = urlparse(self.gifsound_url)
        q = parse_qs(data.query)
        gif_url = str(q.get('gif'))[2:-2]
        print "gif_url: " + gif_url
        if gif_url:
            return gif_url
        else:
            raise AttributeError('gif URL not found in ' + data.geturl())

    def get_convert_url(self):
        '''takes gifsound URL, grabs gif and converts/returns a gfy link'''
        gif_url = self.get_gif_url()
        newurl = "http://upload.gfycat.com/transcode?fetchUrl=" + gif_url
        return newurl

    def get_youtube_url(self):
        '''Grabs a url from gifsound.com and returns
        the youtube url in it'''
        data = urlparse(self.gifsound_url)
        query_data = parse_qs(data.query)
        sound = ''
        if 'sound' in query_data:
            sound = str(query_data.get('sound'))[2:-2]
            return str(sound)
            vid = pafy.new(sound)
            print vid.videoid
            return vid.videoid
        else:
            if 'v' in query_data:
                return str(query_data.get('v'))[2:-2]
            else:
                return "no v or start in query data"

    def get_v(self):
        '''Gets url from gifsound.com and returns the youtube url in it'''
        v = self.get_youtube_url()
        vid = pafy.new(v)
        return vid.videoid

    def get_start(self):
        '''Gets url from gifsound.com and returns the youtube url in it'''
        data = urlparse(self.gifsound_url)
        query_data = parse_qs(data.query)
        if 'start' in query_data:
            print str(query_data['start'])[2:-2]
            start = str(query_data['start'])[3:-2]
            return start
        else:
            return ""

    def check_gfy(self):
        gif_url = self.get_gif_url()
        newurl = "http://gfycat.com/cajax/checkUrl/" + gif_url
        response = urllib2.urlopen(newurl)
        data = json.load(response)
        if data['urlKnown'] is False:
            return 'invalid'
        else:
            return str(data['gfyName'])
