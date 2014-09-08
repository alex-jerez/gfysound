from .forms import SubmissionForm
from django.views.generic.edit import CreateView
from django.http import Http404
#for MakeView
from django.shortcuts import render_to_response, redirect
from django.template import RequestContext
import pafy
from gtool import models
from gtool.models import Gfy
#from gtool.convert import grab_convert_url, grab_youtube_url, make_gfysound_link
from urllib2 import URLError


class SubmissionCreateView(CreateView):
    template_name = 'main.html'
    form_class = SubmissionForm
    success_url = '/'

    def form_valid(self, form):
        #form.send_email()
        return super(SubmissionCreateView, self).form_valid(form)


def make_it(request, v='DGPbHUZQ-VE', g='MeanRevolvingCockerspaniel'):
    '''takes request + two arguments, returns gfysound URL
        v = Youtube video ID
        g = gfycat ID (AdjAdjAnimal)'''
    # get context from request
    context = RequestContext(request)
    #if http method is POST...
    if request.method == 'POST':
        form = SubmissionForm(request.POST)
        if form.is_valid():
            try:
                video = pafy.new(form.cleaned_data['yt_url'])
                videoid = video.videoid
            except URLError:
                video = "http://www.youtube.com/watch?v=nz7sxt9xeJE"
                videoid = "nz7sxt9xeJE"
            g = Gfy(gfycat_url=form.cleaned_data['gfycat_url'])
            #gfyurl = Gfy.get_id(form.cleaned_data['gfycat_url'])
            gfycat = g.get_id()
            mydictionary = {
                'video': video,
                'gfycat': gfycat,
                'form': form,
            }
            newurl = '/%s/%s' % (videoid, gfycat)
           # print "video: %s \ngfycat: http://www.gfycat.com/%s\n" % (video.watchv_url, gfycat)
            return redirect(newurl)
        else:
            print "form is not valid\n"
            print form.errors
    else:
        form = SubmissionForm()
        print v
        try:
            video = pafy.new(v).watchv_url
        except URLError:
            print "URLError again..."
            video = "http://www.youtube.com/watch?v=nz7sxt9xeJE"
        gfycat = 'http://www.gfycat.com/%s' % g
        print "request is GET"
        mydictionary = {
            'form': form,
            'gfycat': g,
            'yt_url': video,
            'gfycat_url': gfycat,
        }
    return render_to_response('main3.html',
                            mydictionary,
                            context_instance=context)


def make_gfysound_url(request):
    '''receive gifsound link, return gfysound link'''
    if request.method == 'POST':
        data = request.POST.data
        gfy_link = grab_convert_url(data)
        yt_link = grab_youtube_url(data)
        newurl = make_gfysound_link(gfy_link, yt_link) # function not yet made
        return redirect(newurl)
    else:
        raise Http404
