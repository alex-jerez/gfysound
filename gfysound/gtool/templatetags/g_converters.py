from django import template
from gtool.models import Gfy
from django.core.urlresolvers import reverse
import pafy


register = template.Library()


@register.simple_tag
def make_url(v, g):
    video = pafy.new(v)
    videoid = video.videoid()
    gfy = Gfy.get_id(g)
    return reverse('make_it', args={'v': videoid, 'g': gfy})
