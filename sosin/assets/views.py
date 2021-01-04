from django.shortcuts import render
from django.views.generic import ListView, DetailView
from .models import Assets

# Create your views here.
class AssetsLV(ListView):
    model = Assets

class AssetsDV(DetailView):
    model = Assets