from django.shortcuts import render

def english(request):
    return render(request, 'atc_site//subjects//english.html', {'user': request.user, 'is_authenticated': request.user.is_authenticated})

def maths(request):
    return render(request, 'atc_site//subjects//maths.html', {'user': request.user, 'is_authenticated': request.user.is_authenticated})

def music(request):
    return render(request, 'atc_site//subjects//music.html', {'user': request.user, 'is_authenticated': request.user.is_authenticated})

def religion(request):
    return render(request, 'atc_site//subjects//religion.html', {'user': request.user, 'is_authenticated': request.user.is_authenticated})

def science(request):
    return render(request, 'atc_site//subjects//science.html', {'user': request.user, 'is_authenticated': request.user.is_authenticated})

def technology(request):
    return render(request, 'atc_site//subjects//technology.html', {'user': request.user, 'is_authenticated': request.user.is_authenticated})