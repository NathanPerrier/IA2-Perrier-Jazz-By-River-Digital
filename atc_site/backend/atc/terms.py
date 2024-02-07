from django.shortcuts import render

def cookie(request):
    return render(request, 'atc_site//terms and policies//cookie_policy.html')

def copyright(request):
    return render(request, 'atc_site//terms and policies//copyright_policy.html')

def privacy(request):
    return render(request, 'atc_site//terms and policies//privacy_policy.html')

def terms_conditions(request):
    return render(request, 'atc_site//terms and policies//terms_and_conditions.html')

def safety(request):
    return render(request, 'atc_site//terms and policies//safety_policy.html')

def terms_of_use(request):
    return render(request, 'atc_site//terms and policies//terms_of_use.html')
