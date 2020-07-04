from .views import *
from django.urls import path



urlpatterns=[
    path('search/',ArticleList.as_view(),name='search'),
    path('type_ahead_wikis/',WikiSearchAPI.as_view(),name='type_ahead_wikis'),
    path('article/',FetchArticle.as_view(), name='article')
]
