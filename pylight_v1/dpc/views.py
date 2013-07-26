from django.http import HttpResponse
from django.template.loader import get_template
from django.template import Context
from django.views.generic.base import TemplateView
from django.shortcuts import render_to_response
from dpc.models import DPCData, Comment
from forms import DPCForm, CommentForm
from django.http import HttpResponseRedirect
from django.core.context_processors import csrf
from django.utils import timezone


def dpcall(request):

    if request.POST:
        form = DPCForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/dpc/all')

    else:
        form = DPCForm()

    args = {}
    args.update(csrf(request))

    args['form'] = form
    args['articles'] = DPCData.objects.all()

    return render_to_response('dpcbase.html',args)


#def all_functions(request):
#    return render_to_response('all_functions.html',
#            {'articles' : DPCData.objects.all()})

def dpcone(request, dpc_id=1):
    args = {}
    item = DPCData.objects.get(id=dpc_id)
    args['article'] = item
    args['articles'] = DPCData.objects.all()
    return render_to_response('dpcone.html',args)

def submit_job(request):
    args = {}
    args['articles'] = DPCData.objects.all()
    total_len = len(DPCData.objects.all())
    args['article'] = DPCData.objects.get(id=total_len)

    return render_to_response('dpc_submit_job.html',args)


def edit_job(request, article_id=1):

    if request.POST:
        form = DPCForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/dpc/all')

    else:
        form = DPCForm()
        args = {}
        args.update(csrf(request))

    item = DPCData.objects.get(id=article_id)
    args['article'] = item
    args['articles'] = DPCData.objects.all()

    args['form'] = form

    return render_to_response('dpc_edit_job.html',args)


"""
def run_job(request, article_id=1):

    #cur_obj = Article.objects.get(id=article_id)

    from job_wrapper import JobWrapper
    JW = JobWrapper()
    JW.readDB(article_id)
    JW.run_job()
    JW.saveDB('Article')

    return render_to_response('see_result.html',
            {'article': Article.objects.get(id=article_id) })


def get_result(request,article_id=1):

    cur_obj = Article.objects.get(id=article_id)
    return render_to_response('get_result.html',
            {'article': Article.objects.get(id=article_id) })
"""

def create(request):
    if request.POST:
        form = DPCForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()

            return HttpResponseRedirect('/dpc/submit_job/')

    else:
        form = DPCForm()

    args = {}
    args.update(csrf(request))

    args['form'] = form

    return render_to_response('create_dpc.html', args)


def delete_job(request, article_id=1):
    obj = DPCData.objects.get(id=article_id)
    obj.delete()
    return HttpResponseRedirect('/dpc/all')


def like_article(request, article_id):
    if article_id:
        a = DPCData.objects.get(id=article_id)
        count = a.likes
        count += 1
        a.likes = count
        a.save()

    return HttpResponseRedirect('/dpc/get/%s' % article_id)


def add_comment(request, article_id):
    a = DPCData.objects.get(id=article_id)

    if request.method == "POST":
        f = CommentForm(request.POST)
        if f.is_valid():
            c = f.save(commit=False)
            c.article = a
            c.save()

            return HttpResponseRedirect('/dpc/get/%s' % article_id)

    else:
        f = CommentForm()

    args = {}
    args.update(csrf(request))

    args['article'] = a
    args['form'] = f

    return render_to_response('dpc_add_comment.html', args)




