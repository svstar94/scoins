from django.forms import ModelForm
from .models import Accounting

class AccountingCreationForm(ModelForm):
    # def __init__(self, *args, **kwargs):
    #     super().__init__(*args, **kwargs)
        # self.fields['username'].disabled = True

    class Meta:
        model = Accounting

        fields = [
            'date', 'iore', 'big_category', 'mid_category', 'sma_category', 'memo', 'amount'
        ]