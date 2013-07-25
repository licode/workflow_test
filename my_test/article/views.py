from django.http import HttpResponse
from django.template.loader import get_template
from django.template import Context
from django.views.generic.base import TemplateView
from django.shortcuts import render_to_response
from article.models import Article, Comment
from forms import ArticleForm, CommentForm
from django.http import HttpResponseRedirect
from django.core.context_processors import csrf
from django.utils import timezone



def articles(request):

    if request.POST:
        form = ArticleForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/articles/all')

    else:
        form = ArticleForm()

    args = {}
    args.update(csrf(request))

    args['form'] = form
    args['articles'] = Article.objects.filter(myname=request.user.username)
    args['fullname'] = request.user.username

    return render_to_response('articles.html',args)


def all_functions(request):
    args = {}
    args['articles'] = Article.objects.filter(myname=request.user.username)
    args['fullname'] = request.user.username
    return render_to_response('all_functions.html',args)

#def all_beamlines(request):
#    return render_to_response('all_beamlines.html')


def article(request, article_id=1):
    args = {}
    item = Article.objects.get(id=article_id)
    args['article'] = item
    args['articles'] = Article.objects.filter(myname=request.user.username)
    args['fullname'] = request.user.username
    return render_to_response('article.html',args)


def submit_job(request):
    args = {}
    #args['article'] = Article.objects.get(id=article_id)

    args['articles'] = Article.objects.all()
    total_len = len(Article.objects.all())

    Article.objects.filter(id=total_len).update(myname=request.user.username)  ###update myname as username

    #article.myname = request.user.username
    args['article'] = Article.objects.get(id=total_len)
    args['articles'] = Article.objects.filter(myname=request.user.username)
    args['fullname'] = request.user.username
    return render_to_response('submit_job.html',args)


def edit_job(request, article_id=1):

    if request.POST:
        form = ArticleForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/articles/all')

    else:
        form = ArticleForm()
        args = {}
        args.update(csrf(request))

    item = Article.objects.get(id=article_id)
    args['article'] = item
    args['articles'] = Article.objects.filter(myname=request.user.username)
    args['fullname'] = request.user.username
    args['form'] = form

    return render_to_response('edit_job.html',args)



def run_job(request, article_id=1):

    args = {}
    item = Article.objects.get(id=article_id)
    args['article'] = item
    args['articles'] = Article.objects.filter(myname=request.user.username)
    args['fullname'] = request.user.username

    from job_manager.job_wrapper import JobWrapper
    JW = JobWrapper()
    JW.readDB("Article", article_id, args['fullname'])
    JW.run_joblist()
    JW.saveDB()

    return render_to_response('see_result.html', args)

"""
def get_result(request,article_id=1):

    cur_obj = Article.objects.get(id=article_id)
    return render_to_response('get_result.html',
            {'article': Article.objects.get(id=article_id) })


def language(request, language='en-gb'):

    response = HttpResponse('setting language to %s' % language)

    response.set_cookie('lang', language)

    request.session['lang'] = language

    return response
"""

def create(request):
    if request.POST:
        form = ArticleForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()

            return HttpResponseRedirect('/articles/submit_job/')

    else:
        form = ArticleForm()

    args = {}
    args.update(csrf(request))

    args['form'] = form
    args['fullname'] = request.user.username

    return render_to_response('create_article.html', args)


def delete_job(request, article_id=1):
    obj = Article.objects.get(id=article_id)
    obj.delete()
    return HttpResponseRedirect('/articles/all')

"""
def like_article(request, article_id):
    if article_id:
        a = Article.objects.get(id=article_id)
        count = a.likes
        count += 1
        a.likes = count
        a.save()

    return HttpResponseRedirect('/articles/get/%s' % article_id)
"""


def add_comment(request, article_id):
    a = Article.objects.get(id=article_id)

    if request.method == "POST":
        f = CommentForm(request.POST)
        if f.is_valid():
            c = f.save(commit=False)
            c.article = a
            c.save()

            return HttpResponseRedirect('/articles/get/%s' % article_id)

    else:
        f = CommentForm()

    args = {}
    args.update(csrf(request))

    args['article'] = a
    args['form'] = f
    args['fullname'] = request.user.username

    return render_to_response('add_comment.html', args)





