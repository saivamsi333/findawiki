import requests
class Utils:
    def get_ws_call(self,url,params):

        response=requests.get(url,params)
        if response and response.status_code==200:
            return response
        else:
            return None

