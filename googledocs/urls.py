from django.conf.urls import url
from . import views
from django.contrib.auth.views import login, logout

urlpatterns = [
    url(r'^$', views.IndexView.as_view(), name='index'),
    url(r'^document_list/$', views.DocumentListView.as_view(), name='document_list'),
    url(r'^login/$', login, name='login'),
    url(r'^logout/$', logout, name='logout'),
    url(r'^register/$', views.register, name='register'),
    url(r'^create_sheet', views.DocumentCreatorView.as_view(doctype='sheet')),
    url(r'^create_doc', views.DocumentCreatorView.as_view(doctype='doc'))
]
