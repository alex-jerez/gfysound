from django.db import models
import re


class Gfy(models.Model):
    """ Class to represent a Gfycat.com object"""
    gfycat_url = models.URLField()

    def get_id(self):
        """gfycat.com URL --> gfycat ID"""
        p = re.compile('(?<=gfycat.com\/)([a-zA-Z]{1,40})')
        id = p.search(self.gfycat_url)
        if id:
            return id.group()
        else:
            print "\n no match for gfycatURL!\n"
            return 'MeanRevolvingCockerspaniel'
