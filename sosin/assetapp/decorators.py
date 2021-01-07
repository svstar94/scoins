from .models import Asset
from django.http import HttpResponseForbidden

def asset_ownership_required(func):
    def decorated(request, *args, **kwargs):
        user = Asset.objects.get(pk=kwargs['pk'])
        if not user == request.user.asset_user:
            return HttpResponseForbidden()
        return func(request, *args, **kwargs)
    return decorated