from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.shortcuts import render, get_object_or_404, redirect
from .models import Post,Category,Profile,Controlpanel
from django.template.response import TemplateResponse
from django.contrib.auth.models import User
from django.core.paginator import Paginator
from .forms import PostForm,ProfileForm
from django.utils.text import slugify
from django.contrib import messages
from django.utils import timezone
from django.conf import settings
from django.db.models import Q


def category_detail(request, category_slug):
    categories = Category.objects.all()
    if category_slug:
        category = get_object_or_404(Category, slug=category_slug)
        posts = Post.objects.filter(category = category).order_by('-timestamp')
    context={
        'category': category,
        'categories':categories,
        'posts' : posts,
    }
    return render(request, 'post_list.html', context)

def user_profile(request, author):
    profile = Profile.objects.get(author__username=author) 
    context ={
        'profile' : profile
    }
    return render(request, 'registration/profile.html', context)

def profile_edit(request,slug=None):
    profile = get_object_or_404(Profile, slug=slug)
    currentUser = request.user
    if not (profile.author == currentUser):
        raise Http404
    else : 
        form = ProfileForm(request.POST or None, request.FILES or None, instance=profile)
        if form.is_valid():
            profile = form.save(commit=False)
            profile.save()
            messages.success(request , "Your changes have been made")
            return HttpResponseRedirect(profile.get_absolute_url())
    context={
        'profile' : profile,
        'form' : form
    }
    return render(request, 'registration/profile_edit.html',context)


def post_list(request):
    try:
        post_list = Post.objects.filter(draft=False).filter(publish__lte = timezone.now()).order_by('-timestamp')
        query = request.GET.get("q")
        if query:
            post_list = post_list.filter(
                                        Q(title__icontains=query)|
                                        Q(content__icontains=query))
        paginator = Paginator(post_list, 5)
        page_number = request.GET.get('page')
        posts = paginator.get_page(page_number)
    except:
         return HttpResponse('No Posts.')
    context = {
            'posts' : posts,
        }
    return render(request, 'post_list.html', context)

def post_detail(request, slug=None):
    categories = Category.objects.all()
    instance = get_object_or_404(Post, slug=slug)
    if instance.draft or instance.publish > timezone.now().date():
        raise Http404
    context = {
        'title' : instance.title,
        'instance' : instance,
        'categories' : categories,
    }
    return render(request, 'post_detail.html', context)

def post_create(request):
    currentUser = request.user
    if not request.user.is_staff or not request.user.is_superuser:
        raise Http404
    form = PostForm(request.POST or None, request.FILES or None)
    if form.is_valid():
        instance = form.save(commit=False)
        instance.author = currentUser
        instance.save()
        return HttpResponseRedirect(instance.get_absolute_url())
        messages.success(request , "Your new post have been made")
    context = {
        'form' : form,
    }
    return render(request, 'post_create.html', context)

def post_update(request, slug=None):
    instance = get_object_or_404(Post, slug=slug)
    currentUser = request.user
    if not (instance.author == currentUser or request.user.is_superuser):
        raise Http404
    form = PostForm(request.POST or None, request.FILES or None, instance=instance)
    if form.is_valid():
        instance = form.save(commit=False)
        instance.save()
        messages.success(request , "Your changes have been made")
        return HttpResponseRedirect(instance.get_absolute_url())
    context = {
        'title' : instance.title,
        'instance' : instance,
        'form' : form,
    }
    return render(request, 'post_update.html', context)

def post_delete(request,id=None):
    instance = get_object_or_404(Post,id=id)
    instance.delete()
    return redirect('/')