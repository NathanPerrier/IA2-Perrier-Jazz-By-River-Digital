from django.shortcuts import render

def cookie(request):
    return render(request, 'atc_site//terms and policies//cookie_policy.html', {'user': request.user, 'is_authenticated': request.user.is_authenticated})

def copyright(request):
    return render(request, 'atc_site//terms and policies//copyright_policy.html', {'user': request.user, 'is_authenticated': request.user.is_authenticated})

def privacy(request):
    return render(request, 'atc_site//terms and policies//privacy_policy.html', {'user': request.user, 'is_authenticated': request.user.is_authenticated})

def terms_conditions(request):
    return render(request, 'atc_site//terms and policies//terms_and_conditions.html', {'user': request.user, 'is_authenticated': request.user.is_authenticated})

def safety(request):
    return render(request, 'atc_site//terms and policies//safety_policy.html', {'user': request.user, 'is_authenticated': request.user.is_authenticated})

def terms_of_use(request):
    return render(request, 'atc_site//terms and policies//terms_of_use.html', {'user': request.user, 'is_authenticated': request.user.is_authenticated})
