from django.contrib.auth import logout,login
from django.shortcuts import redirect


def auth_middleware(get_response):
    def middleware(request):
        returnUrl = request.META['PATH_INFO']

        if not request.session['customer']:
           return redirect(f'login?return_url={returnUrl}')

        response = get_response(request)
        return response

    return middleware



class RestrictAdminUserInFrontend(object):
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.path.find("/admin/") == -1 and request.user.is_authenticated and request.user.is_superuser :
             logout(request)
             return redirect('login')
        response = self.get_response(request)
        return response


# def cart_middleware(get_response):
#     def middleware(request):
#         returnUrl = request.META['PATH_INFO']

#         if not request.session['customer']:
#            return redirect(f'login?return_url={returnUrl}')

#         response = get_response(request)
#         return response

#     return middleware