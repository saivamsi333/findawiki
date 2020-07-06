from django.shortcuts import render
from rest_framework import views
import requests
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



    def get_req_param(self,request,param_key,default_param_value):
        param_value = None
        try:
            if param_key == 'q':
                param_value = request.GET.get(param_key)
            else:
                param_value = int(request.GET.get(param_key))
        except Exception:
            print('Exception while get wiki:', Exception)

        param_value = param_value if param_value else default_param_value
        return param_value

    def construct_req_params(self, request, default_offset, default_limit):
        query = self.get_req_param(request,'q','')
        offset = self.get_req_param(request,'offset',default_offset)
        limit = self.get_req_param(request,'limit',default_limit)
        return  query,limit,offset

    def refine_search_wikis(self,sr_search_value,sr_offset,sr_limit):
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
        query, srlimit, sroffset = self.construct_req_params(request, 0, 5)
        if query:
            data = self.refine_search_wikis(query,sroffset,srlimit)
            return Response(data)
        else:
            data='No required params found'
            return Response(data,status=status.HTTP_404_NOT_FOUND)


class ArticleList(ArticleMixin,views.APIView):
    def get(self,request):
        query,srlimit, sroffset  = self.construct_req_params(request, 0, 50)
        wikis_result = {}

        if query:
            response_data = self.refine_search_wikis(query, sroffset, srlimit)
            wikis_result = response_data
        context = {}
        if wikis_result and wikis_result['query']:
            data = wikis_result['query']['search']
            total_hits = wikis_result['query']['searchinfo']['totalhits']
            pagination_links = []
            pagination = self.construct_pagination_links(data, pagination_links, query, srlimit, sroffset, total_hits)
            context = {
                'totalhits': total_hits,
                'data': data,
                'pagination': pagination
            }

        return render(request,'wiki_search.html',{'context':context})


    def construct_pagination_links(self, data, pagination_links, query, srlimit, sroffset, total_hits):
        offset = 0
        limit = srlimit
        prev = ''
        next = ''
        display_no_of_links = 10

        if not sroffset == 0:
            prev = self.fetch_pagination_link(limit,  query, sroffset)
        range_value = total_hits // 50

        for n in range(range_value):
            offset += limit
            page_obj = {
                'page_no': (n + 1),
                'page_link':self.fetch_pagination_link(limit, query, offset)
            }
            pagination_links.append(page_obj)

        next_offset = (sroffset + limit)

        if next_offset < total_hits:
            next = self.fetch_pagination_link(limit,  query, next_offset)

        return {
                'pagination_links': pagination_links,
                'prev': prev,
                'next': next,
                'display_no_of_links': display_no_of_links
            }

    def fetch_pagination_link(self, limit,  query, sroffset):
        pagination_link = '/search?q=' + query + "&offset=" + str(sroffset) + "&limit=" + str(limit)
        return pagination_link


class FetchArticle(ArticleMixin,View):
    def get(self,request):
        title = self.get_req_param(request,'title','wikipedia')
        url = 'https://en.wikipedia.org/api/rest_v1/page/html/'+title;
        result=self.get_article(url)
        response=HttpResponse(result)
        pdf_download_url = 'https://en.wikipedia.org/api/rest_v1/page/pdf/'+title
        return render(request,'article.html',{'response':response.content,'pdf_download_url':pdf_download_url})



















   
