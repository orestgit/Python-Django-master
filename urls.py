from django.conf.urls import url, include
from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^bucket/(?P<bucket_id>[0-9]+)/$', views.bucket, name='bucket'),
    url(r'^item/(?P<item_id>[0-9]+)/move/(?P<bucket_id>[0-9]+)/$',
        views.move, name='move'),
    url(r'^item/(?P<item_id>[0-9]+)/$', views.item, name='item'),
    url(r'^add/', views.add, name='add'),
    url(r'^bucket/(?P<bucket_id>[0-9]+)/add/$', views.add, name='addtobucket'),
    url(r'^search/$', views.search, name='search'),
    url(r'^accounts/', include('django.contrib.auth.urls'))
]
