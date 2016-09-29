"""blognerds URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.9/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf import settings
from django.conf.urls import include, url
from django.conf.urls.static import static
from django.contrib import admin
from dashing.utils import router

# in django urls always import just one view, because multiple view import may cause url to break
# class base views have a different view writting pattern from function base view in the urls
# function based views runs as strings and they run like this url(r'^about/', 'posts.views.about_us', name='about'),
# class based views runs as direct quote and not a string, also like this url(r'^about/', posts.views.about_us, name='about'),

from accounts import views
from notifications import views
from questions import views
from videos import views
from accounts.views import (auth_login, register_view, auth_logout)

urlpatterns = [

    # url patterns for admin login
    url(r'^admin/officialnerds/', admin.site.urls),


    # url patterns for video content manager
    url(r'^staff/$', "videos.views.staff_home", name='staff'),
    url(r'^courses/$', 'videos.views.category_list', name='projects'),
    url(r'^courses/(?P<cat_slug>[\w-]+)/$', 'videos.views.category_detail', name='project_detail'),
    url(r'^courses/(?P<cat_slug>[\w-]+)/(?P<vid_slug>[\w-]+)/$', 'videos.views.video_detail', name='video_detail'),

    #url patterns for notifications stuffs
    url(r'^notifications/$', 'notifications.views.all', name='notifications_all'),
    url(r'^notifications/ajax/$', 'notifications.views.get_notifications_ajax', name='get_notifications_ajax'),
    url(r'^notifications/(?P<id>\d+)/$', 'notifications.views.all', name='notifications_read'),
    # some url here again


    # url patterns for site utilities
    url(r'^dashboard/', include(router.urls)),
    url(r'^contact/', 'newsletter.views.contact_us', name='contact'),
    url(r'^about/', 'posts.views.about_us', name='about'),
    url(r'^service/', 'posts.views.services', name='service'),


    #url(r'^projects/', include('suggest_projects.urls', namespace='projects')),


    # url patterns for authentication systems
    url(r'^login/', 'accounts.views.auth_login', name='login'),
    url(r'^logout/', 'accounts.views.auth_logout', name='logout'),


    # url patterns for site registration system
    url(r'^register/', 'accounts.views.register_view', name='register'),


    #url patterns for content stuffs
    url(r'^blog/', include ("posts.urls_2", namespace= 'blogs')),
    url(r'^comments/', include ("comments.urls", namespace= 'comments')),
    url(r'^', include ("posts.urls", namespace= 'posts')),

    #url patterns for video content stuffs
    url(r'^question/(?P<id>\d+)/$', 'questions.views.question_thread', name='question_thread'),
    url(r'^question/create/$', 'questions.views.question_create_view', name='question_create'),

]



if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root = settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)
