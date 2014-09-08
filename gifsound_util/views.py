from gifsound_util.models import Gifsound
from django.template import RequestContext
from django.http import HttpResponseRedirect
from .forms import GifsoundForm
from django.shortcuts import render_to_response
from django.views.generic import FormView


def gif2gfy(request):
    url = request.POST.get('gifsound_url')
    print str(url)
    g = Gifsound(gifsound_url=url)
    convert_url = g.get_convert_url()
    yt_url = g.get_youtube_url()
    v = g.get_v()
    start = g.get_start()
    gfy = g.check_gfy()
    context = {'convert_url': convert_url,
               'yt_url': yt_url,
               'v': v,
               'start': start,
               'gfy': gfy}
    print "gfy value is:" + gfy
    print "v value is:" + str(v)
    if gfy == 'invalid' or v == "":
        return render_to_response('invalid_gfy.html',
                                  context,
                                  context_instance=RequestContext(request))
    else:
        if start != "":
            v += ("&" + start)
        newurl = 'http://gfysound.com/' + \
            v + "/" + gfy
        return HttpResponseRedirect(newurl)


class gifform(FormView):
    template_name = 'gifsound_form.html'
    form_class = GifsoundForm
    success_url = '/test/'

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super(gifform, self).get_context_data(**kwargs)
        # Add in a QuerySet
        context['url'] = \
            'http://gifsound.com/?gif=i.imgur.com/uLhzDfg.gif&v=WwG2newDukk'
        return context
