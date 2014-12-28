from .forms import SubmissionForm
from django.views.generic.edit import CreateView
#for MakeView
from django.shortcuts import render_to_response, redirect
from django.template import RequestContext
import pafy
from gtool import models
from gtool.models import Gfy
from urllib2 import URLError
from settings import production
from django.contrib.sites.shortcuts import get_current_site


class SubmissionCreateView(CreateView):
    template_name = 'main.html'
    form_class = SubmissionForm
    success_url = '/'

    def form_valid(self, form):
        return super(SubmissionCreateView, self).form_valid(form)


def make_it(request, v='DGPbHUZQ-VE', g='MeanRevolvingCockerspaniel', st=0):
    ''' st = start time (default 0)
        v = Youtube video ID
        g = gfycat ID (AdjAdjAnimal)'''
    # get context from request
    context = RequestContext(request)
    sitename = get_current_domain(request)
    print(sitename)
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
            st = form.cleaned_data['starttime']
            #gfyurl = Gfy.get_id(form.cleaned_data['gfycat_url'])
            gfycat = g.get_id()
            mydictionary = {
                'video': video,
                'videoid': videoid,
                'gfycat': gfycat,
                'form': form,
                'st': st,
                'v': v,
            }
            if st == 0:
                newurl = '/%s/%s' % (videoid, gfycat)
            else:
                newurl = '/%s&%d/%s' % (videoid, st, gfycat)
            mydictionary['newurl']=newurl
           # print "video: %s \ngfycat: http://www.gfycat.com/%s\n" % (video.watchv_url, gfycat)
            return redirect(newurl)
        else:
            print "form is not valid\n"
            print form.errors
            return redirect('/error/')
    else:
        form = SubmissionForm()
        print v
        try:
            video = pafy.new(v).watchv_url
        except (URLError, AttributeError):
            print "URLError again..."
            video = ""#http://www.youtube.com/watch?v=nz7sxt9xeJE"
        gfycat = 'http://www.gfycat.com/%s' % g
        print "request is GET"
        mydictionary = {
            'form': form,
            'gfycat': g,
            'yt_url': video,
            'gfycat_url': gfycat,
            'st': st,
            'v': v,
            'SITE': sitename.domain, 
        }
    return render_to_response('main3.html',
                            mydictionary,
                            context_instance=context)
