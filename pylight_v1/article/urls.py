from django.conf.urls import patterns, include, url


urlpatterns = patterns('article.views',
    url(r'^all_functions/$', 'all_functions'),
    #url(r'^all_beamlines/$', 'all_beamlines'),
    url(r'^all/$', 'articles'),

    url(r'^get/(?P<article_id>\d+)/$', 'article'),
    url(r'^run/(?P<article_id>\d+)/$', 'run_job'),
    #url(r'^language/(?P<language>[a-z\-]+)/$', 'language'),
    url(r'^create/$', 'create'),
    #url(r'^like/(?P<article_id>\d+)/$', 'like_article'),
    url(r'^add_comment/(?P<article_id>\d+)/$', 'add_comment'),
    url(r'^see_result/(?P<article_id>\d+)/$', 'see_result'),  #see results after submission
    #url(r'^get_result/(?P<article_id>\d+)/$', 'get_result'),
    url(r'^delete/(?P<article_id>\d+)/$', 'delete_job'),
    url(r'^edit_job/(?P<article_id>\d+)/$', 'edit_job'),
    url(r'^submit_job/$', 'submit_job'),
)
