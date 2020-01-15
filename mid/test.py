from django.utils.deprecation import MiddlewareMixin
from django.http import JsonResponse

PassUrl = set( ["/login","/resgiter", "/helloworld"] )

class Token (MiddlewareMixin):
    def process_request(self, request):
        # print( dir(request) )
        if request.path in  PassUrl:
            return None
        hasToken = "Authorization" in request.headers
        StatusFaile = JsonResponse( { "code": -123, "msg": "非法访问" } ,status = 400)
        if hasToken :
            token = request.headers.token
            '''
                token验证逻辑
            '''
            return None
        return StatusFaile