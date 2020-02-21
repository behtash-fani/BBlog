from django.http import HttpResponseRedirect,Http404
from django.shortcuts import get_object_or_404
from .models import Profile



def profile_info(request):
    if request.user.is_authenticated:
        profile = Profile.objects.get(author__username=request.user)
        return {'profile':profile}
    return {}

        