from .views import *
from django.urls import path



urlpatterns=[
    path('search/',wiki_search,name='search'),
    path('api/',WikiSearchAPI.as_view(),name='api'),
    path('fetch_api/',FetchArticle.as_view(),name='fetch'),
    path('article/',FetchArticle.as_view()),
    path('pdf/',PdfGenerator.as_view(),name='pdf')
]
