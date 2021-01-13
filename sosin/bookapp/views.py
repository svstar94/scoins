from django.shortcuts import render
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
# Create your views here.

from .models import *
from .forms import AccountingCreationForm
from django.urls import reverse, reverse_lazy
from django.views.generic import CreateView, DetailView, DeleteView
from django.contrib.auth.models import User

class BookCreateView(CreateView):
    model = Accounting
    context_object_name = 'target_book'
    form_class = AccountingCreationForm
    success_url = reverse_lazy('bookapp:detail')
    template_name = 'bookapp/create.html'
    
    def form_valid(self, form):
        temp_book = form.save(commit=False)
        temp_book.user = self.request.user
        temp_book.save()
        form.clean()
        return super().form_valid(form)
    
    def get_success_url(self):
        return reverse('bookapp:detail')

from assetapp.models import Asset, id2ctg
from scoin.tools import get_model_fields

# @method_decorator(login_required, 'get')
from django.views.generic import View

def BookDetailView(request):
    if request.user.book.exists():
        book_list = request.user.book.filter(user_id=request.user.id)
    else:
        book_list = None

    return render(request, template_name='bookapp/detail.html', context={'target_user' : request.user, 'book_list':book_list})

from datetime import datetime

def get_text(model):
    text = model.date + \
            '수입' if model.iore else '지출' + \
            b_id2ctg[model.big_category] if model.big_category else '' + \
            m_id2ctg[model.mid_category] if model.mid_category else '' + \
            s_id2ctg[model.sma_category] if model.sma_category else '' + \
            model.memo + model.amount
    return text

b_id2ctg = ['자유입출금']
m_id2ctg = ['수익', '성장', '생활', '여가', '기타']
s_id2ctg = [['월급', '외주', '보너스', '이익배당금'],
            ['자기계발'],
            ['식사', '미용', '의복', '생활용품', '통신비', '교통비', '주거비'],
            ['커피', '게임', ' 보험', '여행', '문화'],
            ['기타', '병원', '경조사', '애완동물']]


class BookDeleteView(DeleteView):
    model = Accounting
    context_object_name = 'target_book'
    template_name = 'bookapp/delete.html'

    def get_success_url(self):
        return reverse('bookapp:detail')
