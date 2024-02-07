from django.shortcuts import render

def english(request):
    return render(request, 'atc_site//subjects//english.html')

def maths(request):
    return render(request, 'atc_site//subjects//maths.html')

def music(request):
    return render(request, 'atc_site//subjects//music.html')

def religion(request):
    return render(request, 'atc_site//subjects//religion.html')

def science(request):
    return render(request, 'atc_site//subjects//science.html')

def technology(request):
    return render(request, 'atc_site//subjects//technology.html')