from django.conf.urls import url
from django.contrib import admin


from comments.views import (
    comment_thread,
)


urlpatterns = [
    url(r'^(?P<id>\d+)/$', comment_thread, name='thread'),
    #url(r'^(?P<slug>[\w-]+)/delete/$', comment_delete),
]


#####################################################################################
#                       This is for blog_list.html alone                            #
#                                                                                   #
#####################################################################################




#urlpatterns = [
#    url(r'^$', post_list, name='list'),
#    url(r'^create/$', post_create),
#    url(r'^(?P<id>\d+)/$', post_detail, name='detail'),
#    url(r'^(?P<id>\d+)/edit/$', post_update, name='update'),
#    url(r'^(?P<id>\d+)/delete/$', post_delete),
#]