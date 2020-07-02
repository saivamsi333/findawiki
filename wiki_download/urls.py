from .views import *
from django.urls import path



urlpatterns=[
    path('search/',wiki_search,name='search'),
    path('api/',WikiSearchAPI.as_view(),name='api')
]
