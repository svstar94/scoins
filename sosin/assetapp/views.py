from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.views.generic import CreateView, UpdateView
from django.shortcuts import render
from .forms import AssetCreationForm
from django.urls import reverse, reverse_lazy

from .models import Asset

from .decorators import asset_ownership_required

# Create your views here.
class AssetCreateView(CreateView):
    model = Asset
    context_object_name = 'target_asset'
    form_class = AssetCreationForm
    success_url = reverse_lazy('accountapp:detail')
    template_name = 'assetapp/create.html'

    def form_valid(self, form):
        temp_asset=form.save(commit=False)
        temp_asset.user = self.request.user
        temp_asset.save()
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('accountapp:detail', kwargs={'pk':self.object.user.pk})

@method_decorator(asset_ownership_required, 'get')
@method_decorator(asset_ownership_required, 'post')
class AssetUpdateView(UpdateView):
    model = Asset
    context_object_name = 'target_asset'
    form_class = AssetCreationForm
    template_name = 'assetapp/update.html'

    def get_success_url(self):
        return reverse('accountapp:detail', kwargs={'pk':self.object.user.pk})
