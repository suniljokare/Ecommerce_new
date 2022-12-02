
from django.shortcuts import redirect
from django.shortcuts import render,HttpResponseRedirect,redirect,HttpResponse


def auth_middleware(get_response):

    def middleware(request):
        customer = request.session.get('customer')
 
        # returnUrl = request.META.get('HTTP_REFERER')
        # returnUrl = request.META['PATH_INFO']

        if  customer==None:
            return redirect('login')
        #    return redirect(f'login?return_url={returnUrl}')
    
        response = get_response(request)
        return response

    return middleware   


