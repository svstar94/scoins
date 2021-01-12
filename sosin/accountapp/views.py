from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.urls import reverse, reverse_lazy

# Create your views here.

def hello_world(request):
    if request.method == 'POST':
        return HttpResponseRedirect(reverse('accountapp:hello_world'))
    else:
        hello_world_list = ['aa', 'bb']
        return render(request, 'accountapp/hello_world.html', context={'hello_world_list': hello_world_list})


from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views.generic import CreateView, DetailView, UpdateView, DeleteView
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .decorators import account_ownership_required

has_ownership = [login_required, account_ownership_required]

class AccountCreateView(CreateView):
    model = User
    form_class = UserCreationForm
    template_name = 'accountapp/create.html'
    success_url = reverse_lazy('accountapp:login')    

from assetapp.models import Asset, id2ctg
from scoin.tools import get_model_fields
class AccountDetailView(DetailView):
    model = User
    context_object_name = 'target_user'
    template_name = 'accountapp/detail.html'

    def get_context_data(self, **kwargs):
        context = super(AccountDetailView, self).get_context_data(**kwargs)
        print(self.object.username)
        try:
            asset_list = list(Asset.objects.filter(id=self.object.asset_user.id).values()[0].values())[3:]
            asset_field = [id2ctg[field.name] for field in list(get_model_fields(Asset))[3:]]
            context['user_asset'] = list(zip(asset_field, asset_list))
            context['asset_object'] = Asset.objects.filter(id=self.object.asset_user.id)[0]
        except:
            pass
        
        return context

from .forms import AccountUpdateForm

@method_decorator(has_ownership, 'get')
@method_decorator(has_ownership, 'post')
class AccountUpdateView(UpdateView):
    model = User
    form_class = AccountUpdateForm
    context_object_name = 'target_user'
    template_name = 'accountapp/update.html'
    
    def get_success_url(self):
        return reverse_lazy('accountapp:detail', kwargs={'pk':self.object.pk})


@method_decorator(has_ownership, 'get')
@method_decorator(has_ownership, 'post')
class AccountDeleteView(DeleteView):
    model = User
    success_url = reverse_lazy('accountapp:login')
    context_object_name = 'target_user'
    template_name = 'accountapp/delete.html'
