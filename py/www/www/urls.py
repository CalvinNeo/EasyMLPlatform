"""www URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/dev/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add an import:  from blog import urls as blog_urls
    2. Add a URL to urlpatterns:  url(r'^blog/', include(blog_urls))
"""
from django.conf.urls import patterns, include, url
from django.conf import settings
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'mysite.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls))
    ,url(r'^static/(?P<path>.*)$','django.views.static.serve',{'document_root':settings.STATIC_ROOT})
    ,url(r'^$', 'www.views.index')
    ,url(r'^index/(\w+)/$', 'www.views.index', name = 'index')
    ,url(r'^index/$', 'www.views.index', name = 'index')
    ,url(r'^api/(\w+)/$', 'www.views.api', name = 'api')
    ,url(r'^login/$', 'www.views.login', name = 'login')
    ,url(r'^logout/$', 'www.views.logout', name = 'logout')
    ,url(r'^accounts/login/$', 'www.views.login', name = 'login')
    # ,static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
)

# urlpatterns = [
#     url(r'^admin/', admin.site.urls),
#     url(r'^$', 'www.views.first_page')
# ]
