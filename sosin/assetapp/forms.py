from django.forms import ModelForm
from .models import Asset

class AssetCreationForm(ModelForm):
    # def __init__(self, *args, **kwargs):
    #     super().__init__(*args, **kwargs)
        # self.fields['username'].disabled = True

    class Meta:
        model = Asset

        fields = [
            'freedps', 'stock', 'installment', 'house_sbsc', 'cma', 'invest', 'house' ,'debt'
        ]