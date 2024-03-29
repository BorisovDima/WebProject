"""mysite URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf.urls.i18n import i18n_patterns
from django.contrib.sitemaps.views import sitemap


urlpatterns = [
    path('sitemap.xml', sitemap, name='django.contrib.sitemaps.views.sitemap'),
    path('admin/', admin.site.urls, name='admin'),
    path('', include('project.apps.search.urls')),
    path('', include('project.apps.blog.urls')),
    path('', include('project.apps.myauth.urls')),
    path('', include('project.apps.account.urls')),
    path('', include('project.apps.chat.urls')),
    path('', include('social_django.urls', namespace='social')),
    path('api/', include('project.apps.delete_app.urls')),
    path('api/', include('project.apps.ajax_utils.urls')),
    path('api/', include('project.apps.like_dislike.urls')),
    path('api/', include('project.apps.comments.urls')),
    path('api/', include('project.apps.autocomplete.urls'))

]

urlpatterns += i18n_patterns(path('info/', include('project.apps.info.urls')))
