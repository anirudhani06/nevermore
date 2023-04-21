from django.shortcuts import redirect


def is_unauthenticate(view_func):
    def wrapper_func(request,*args,**kwargs):
        if request.user is not None:
            return view_func(request,*args,**kwargs)
        else:
            return redirect('home')
    
    return wrapper_func

