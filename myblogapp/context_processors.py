from django.http import HttpResponseRedirect,Http404
from django.shortcuts import get_object_or_404
from .models import Profile,Controlpanel,Category,Post



def profile_info(request):
    blog_settings = Controlpanel.objects.all()
    categories = Category.objects.all()
    if request.user.is_authenticated:
        profile = Profile.objects.get(author__username=request.user)
        return {
            'profile':profile,
            'blog_settings':blog_settings,
            'categories' : categories
            }
    return {
        'blog_settings':blog_settings,
        'categories' : categories
        }