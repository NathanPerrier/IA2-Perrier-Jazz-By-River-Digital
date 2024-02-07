from django.contrib.auth import login as loginRequest
from django.contrib.auth import authenticate
from ....models import CustomUserManager
from ...main import login_page, index

def loginView(request, error=None):
    if request.method == 'POST':
        user = authenticate(request, email=request.POST['email'], password=request.POST['password']) #CustomUserManager().authenticate(email=request.POST['email'], password=request.POST['password']) 
        if user is not None:
            user.backend = 'django.contrib.auth.backends.ModelBackend'
            loginRequest(request, user, backend='django.contrib.auth.backends.ModelBackend')
            # auth_login(request, user)
            request.session['user_id'] = user.id
            return index(request)
        return login_page(request, error='Invalid Login')
    return login_page(request)