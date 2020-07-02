from django.shortcuts import render
from wikipediaapi import Wikipedia
from rest_framework import views
#import requests
import wikipedia
from .models import *
from .serializers import *
from .utils import *
from rest_framework.response import Response


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
        params={
            'action':'query',
            'generator' :'random',
            'srsearch':query,
            'format':'json',
            'list':'search',
            'grnnamespace':'0',
            'prop':'info|extracts',
            'inprop':'url'

        }

        # data=Utils.get_ws_call(url,params)
        # serializer=WikiSerializer(data)
        response = requests.get(url, params)
        if response and response.status_code == 200:
            print(response)
            data = response.json()
        else:
            print('error')

        return Response(data)






   
