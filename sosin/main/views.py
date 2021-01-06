from django.shortcuts import render
from django.views.generic import TemplateView

# Create your views here.

class MainView(TemplateView):
    template_name = 'main.html'

# Create your views here.
from .models import *
from django.http import HttpResponseRedirect
from django.urls import reverse

def main_view(request):

    if request.method == 'POST':
        
        # temp = request.POST.get('hello_world_input')

        # return HttpResponseRedirect(reverse('accountapp:hello_world'))
        return render(request, 'mainapp/main.html', context={'hello_world_list': Coins.date})
    
    else:
        coins_list = Coins.objects.all()
        return render(request, 'main/main.html', context={'asset_list': coins_list})
