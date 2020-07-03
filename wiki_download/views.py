from django.shortcuts import render
from wikipediaapi import Wikipedia
from rest_framework import views
#import requests
import wikipedia
from .models import *
from .serializers import *
from .utils import *
from rest_framework.response import Response
from django.http import HttpResponse
import json
from io import BytesIO
from django.template.loader import get_template
from xhtml2pdf import pisa
from django.views import View

# Create your views here.

def wiki_search(request):

      return render(request,'wiki_search.html')

class WikiSearchAPI(views.APIView):

    def get(self,request):
        url='https://en.wikipedia.org/w/api.php'
        query=' '
        try:
            query=request.GET.get('q')
        except Exception:

            print('Exception while get wiki:',Exception)

        query = query if query else ' '
        # params={
        #     'action':'query',
        #     'generator' :'random',
        #     'srsearch':query,
        #     'format':'json',
        #     'list':'search',
        #
        #     'grnnamespace':'0',
        #
        #     'prop':'info|extracts',
        #     'inprop':'url'
        #
        # }
        params={
            'action': 'query',
            'srsearch': event.target.value,
            'format': 'json',
            'list': 'search',
            'srlimit': 5
        }

        response = requests.get(url, params)
        if response and response.status_code == 200:
            #print(response)
            data = response.json()
        else:
            print('error')
        pagesArray = []
        # for id in data['query']['pages']:
        #     pagesArray.append(data['query']['pages'][id])

        data['pages'] = pagesArray;

        return Response(data)

class ArticleDetailMixin(object):
    url = 'http://en.wikipedia.org/w/api.php?action=query&prop=extracts|info&exintro&titles=google&format=json&explaintext&redirects&inprop=url&indexpageids'
    data = requests.get(url).json()
    def get_article(self):


        result = requests.get(self.data['query']['pages']['1092923']['fullurl'])

        return result

class FetchArticle(ArticleDetailMixin,View):
    def get(self,request):
        #url='http://en.wikipedia.org/w/api.php?action=query&prop=extracts|info&exintro&titles=google&format=json&explaintext&redirects&inprop=url&indexpageids'
        #data=requests.get(url).json()
        result=self.get_article()


        #result=requests.get(data['query']['pages']['1092923']['fullurl'])
        #result=result.strip('\n').strip('\t')
        response=HttpResponse(result)
        # stringHtml = response.content.strip('\n')
        # stringHtml = stringHtml.strip('\t')
        response.content = response.content.strip(bytes('\r\t','utf-8'))
        response.content = response.content.strip(bytes('\r\n','utf-8'))
        return render(request,'article.html',{'response':response.content})
        #return HttpResponse(result)


class PdfGenerator(ArticleDetailMixin,views.APIView):

    def get(self,request):
        content=get_template()
        pdf_file=render_to_pdf('pdf/article.pdf',data=content)
        return HttpResponse(pdf_file,content_type='application/pdf')



















   
