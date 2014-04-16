from .forms import SubmissionForm
from django.views.generic.edit import CreateView
#for MakeView
from django.shortcuts import render_to_response, redirect
from django.template import RequestContext
import pafy
from gtool import models
from gtool.models import Gfy
from urllib2 import URLError


class SubmissionCreateView(CreateView):
    template_name = 'main.html'
    form_class = SubmissionForm
    success_url = '/'

    def form_valid(self, form):
        #form.send_email()
        return super(SubmissionCreateView, self).form_valid(form)


def make_it(request, v='DGPbHUZQ-VE', g='MeanRevolvingCockerspaniel', st=0):
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
            starttime = form.cleaned_data['starttime']
            mydictionary = {
                'video': video,
                'gfycat': gfycat,
                'form': form,
                'starttime': starttime
            }
            newurl = '/%s&%d/%s' % (videoid, starttime, gfycat)
           # print "video: %s \ngfycat: http://www.gfycat.com/%s\n" % (video.watchv_url, gfycat)
            return redirect(newurl)
        else:
            print "form is not valid\n"
            print form.errors
    else:
        form = SubmissionForm()
        print v
        try:
            video = pafy.new(v)
            videoid = video.videoid
        except URLError:
            print "URLError..."
            video = "http://www.youtube.com/watch?v=nz7sxt9xeJE"
            videoid = "nz7sxt9xeJE"
        gfycat = 'http://www.gfycat.com/%s' % g
        print "request is GET"
        mydictionary = {
            'form': form,
            'gfycat': g,
            'video': videoid,
            'yt_url': video.watchv_url,
            'gfycat_url': gfycat,
            'starttime': st,
        }
    return render_to_response('main3.html',
                            mydictionary,
                            context_instance=context)
