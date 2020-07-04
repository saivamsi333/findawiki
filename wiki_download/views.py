from django.shortcuts import render
#from wikipediaapi import Wikipedia
from rest_framework import views
import requests
import wikipedia
from .utils import *
from rest_framework.response import Response
from django.http import HttpResponse
import json
from io import BytesIO
from django.template.loader import get_template
from xhtml2pdf import pisa
from django.views import View
from rest_framework import status


class ArticleMixin(object):
    def get_article(self,url):
        result = requests.get(url)
        return result

    def refineSearchWikis(self,sr_search_value,sr_offset,sr_limit):
        url='https://en.wikipedia.org/w/api.php'
        params = {
            'action': 'query',
            'srsearch': sr_search_value,
            'format': 'json',
            'list': 'search',
            'srlimit': sr_limit,
            'sroffset':sr_offset
        }

        response = get_ws_call(self,url,params)
        return  response.json()

class WikiSearchAPI(ArticleMixin,views.APIView):

    def get(self,request):
        url='https://en.wikipedia.org/w/api.php'
        query=' '
        try:
            query=request.GET.get('q')
        except Exception:
            print('Exception while get wiki:',Exception)

        srlimit=5
        try:
            srlimit=int(request.GET.get('limit'))
        except Exception:
            print('Exception while get wiki:',Exception)

        sroffset = 0
        try:
            sroffset=int(request.GET.get('offset'))
        except Exception:
            print('Exception while get wiki:',Exception)

        query = query if query else ' '
        if query:
            data = self.refineSearchWikis(query,sroffset,srlimit)
            return Response(data)
        else:
            data='No required params found'
            return Response(data,status=status.HTTP_404_NOT_FOUND)


class ArticleList(ArticleMixin,views.APIView):
    def get(self,request):
        url = 'http://en.wikipedia.org/w/api.php?'
        query = ' '
        try:
            query = request.GET.get('q')
        except Exception:
            print('Exception while get wiki:', Exception)
            query = ''

        srlimit = 20
        try:
            srlimit = int(request.GET.get('limit'))
        except Exception:
            print('Exception while get wiki:', Exception)
            srlimit = 50

        sroffset = 0
        try:
            sroffset = int(request.GET.get('offset'))
        except Exception:
            print('Exception while get wiki:', Exception)
            sroffset = 0
        wikis_result = {}
        query = query if query else ' '
        srlimit = srlimit if srlimit else 50
        sroffset = sroffset if sroffset else 0
        if query:
            response_data = self.refineSearchWikis(query, sroffset, srlimit)
            wikis_result = response_data

        if wikis_result and wikis_result['query']:
            data = wikis_result['query']['search']
            total_hits = wikis_result['query']['searchinfo']['totalhits']
            pagination_links = []
            offset = 0
            limit = srlimit
            prev = ''
            next = ''
            display_no_of_links = 10
            if not sroffset == 0:
                prev = '/search?q='+query+"&offset="+str(sroffset)+"&limit="+str(limit)
            range_value = total_hits//20
            for n in range(range_value):
                offset += limit
                page_obj = {
                    'page_no':(n+1),
                    'page_link' : '/search?q=' + query + "&offset=" + str(offset) + "&limit=" + str(limit)
                }
                pagination_links.append(page_obj)
            next_offset = (sroffset+limit);
            if next_offset < total_hits:
                next = '/search?q='+query+"&offset="+str(next_offset)+"&limit="+str(limit)
            context = {
                'totalhits':total_hits,
                'data':data,
                'pagination': {
                    'pagination_links':pagination_links,
                    'prev':prev,
                    'next':next,
                    'display_no_of_links':display_no_of_links
                }
            }
            return render(request,'wiki_search.html',{'context':context})



class FetchArticle(ArticleMixin,View):
    def get(self,request):
        title = ''
        try:
            title = request.GET.get('title');
        except Exception:
            title = ''
            print('error while FetchArticle')
        url = 'https://en.wikipedia.org/api/rest_v1/page/html/'+title;
        result=self.get_article(url)
        response=HttpResponse(result)
        pdf_download_url = 'https://en.wikipedia.org/api/rest_v1/page/pdf/'+title
        return render(request,'article.html',{'response':response.content,'pdf_download_url':pdf_download_url})



















   
