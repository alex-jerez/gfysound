from django.db import models
from django.core.validators import RegexValidator
import pafy
from gtool.models import Gfy


class Submission(models.Model):
    yt_url = models.URLField(
        default="http://www.youtube.com/watch?v=7WauUpq4N8I")
    gfycat_url = models.URLField(
        default='http://gfycat.com/MeanRevolvingCockerspaniel',
        validators=[
            RegexValidator(
                regex='^https?:\/\/([a-zA-Z\d-]+\.){0,}gfycat\.com',
                message="Enter a valid gfycat.com URL.",
                code='invalid_gfycat_url'
            ),
        ]
    )
    title = models.CharField(max_length=100, default="Untitled")
    starttime = models.IntegerField(default=0)

    def getYoutubeID(self):
        # Youtube URL => Youtube ID
        y = pafy.new(self.yt_url)
        return y.videoid
    def getGfyID(self):
        return Gfy.get_id(self.gfycat_url)
