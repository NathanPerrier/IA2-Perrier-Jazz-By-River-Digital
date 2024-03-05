from django.shortcuts import render, redirect

def superuser_required(request):
    def decorator(func):
        def wrapper(request, *args, **kwargs):
            if request.user.is_superuser:
                return func(*args, **kwargs)
            return render(request, 'atc_site//error.html', {'user': request.user, 'is_authenticated': request.user.is_authenticated, 'error' : '403', 'title' : 'Access Forbidden', 'desc' : 'You do not have permission to access this page. Please contact the administrator if you believe this is an error.'})
        return wrapper
    return decorator

def login_required(request):
    def decorator(func):
        def wrapper(request, *args, **kwargs):
            if request.user:
                return func(*args, **kwargs)
            return redirect('login')
        return wrapper
    return decorator