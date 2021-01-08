from django.shortcuts import render

# Create your views here.
from .models import *

from django.views.generic import ListView, DetailView, View
import datetime
from django.contrib.auth.models import User

from django.shortcuts import render
from assetapp.models import Asset, id2ctg
from scoin.tools import get_model_fields

class HomeView(ListView):
    model = News
    template_name = 'homeapp/home.html'
    context_object_name = 'news_list'
    paginate_by = 5

    def get_context_data(self, **kwargs):
        context = super(HomeView, self).get_context_data(**kwargs)
        labels = [id2ctg[field.name] for field in list(get_model_fields(Asset))[3:]]
        context['coin_list'] = Coin.objects.all()
        context['stock_list'] = Stock.objects.all()

        if self.request.user.is_authenticated:
            datas = Asset.objects.filter(id=self.request.user.asset_user.id).values()[0]
            
            pie_labels = []
            pie_datas = []
            for i, k in enumerate(datas):
                if i < 3: continue
                if datas[k]:
                    pie_labels.append(id2ctg[k])
                    pie_datas.append(datas[k])

            context['target_user'] = self.request.user
            context['asset_list'] = Asset.objects.filter(id=self.request.user.asset_user.id).values()[0].values()
            context['data'] = pie_datas
            context['labels'] = pie_labels

        return context

