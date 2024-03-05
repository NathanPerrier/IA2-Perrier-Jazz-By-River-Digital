""" Dynamic form that gets displayed when the chatbot access/edits or deletes any data. will appear with info and confirm and cancel buttons. """
from django import forms
from django.http import JsonResponse
from django.views import View

class UniversalForm(forms.Form):
    model_name = forms.CharField(max_length=200)
    action = forms.CharField(max_length=200)
    data = forms.JSONField()

class UniversalFormView(View):
    form_class = UniversalForm
    template_name = 'universal_form.html'

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            model_name = form.cleaned_data['model_name']
            action = form.cleaned_data['action']
            data = form.cleaned_data['data']

            #* handle the data based on the model_name and action

            return JsonResponse({'status': 'success'})

        return JsonResponse({'status': 'error', 'errors': form.errors})