from django.db.models.signals import post_save
from django.db.models.signals import pre_save
from django.contrib.auth.models import User
from django.utils.text import slugify
from django.conf import settings
from django.urls import reverse
from datetime import datetime
from django.db import models



class Category(models.Model):
    title = models.CharField(max_length = 255)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Created at",blank=True,null=True)
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Updated at",blank=True,null=True)
    slug = models.SlugField(max_length = 255,unique=True,null=True)

    class Meta:
        verbose_name = "Category"
        verbose_name_plural = "Categories"
        ordering = ['title']

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('category_detail', kwargs={'slug': self.slug})

class Profile(models.Model):
    author = models.ForeignKey(settings.AUTH_USER_MODEL, blank=True, null=True, on_delete=models.CASCADE)
    slug = models.SlugField(max_length = 255,unique=True,null=True)
    email = models.EmailField(max_length=254, blank=True)
    avatar = models.FileField(null=True, blank=True)
    website = models.URLField(blank=True, null=True)
    bio = models.TextField(blank=True,null=True)
    gender_choice = (
            ('Female', 'Female'),
            ('Male', 'Male'),
        )
    gender = models.CharField(max_length=30, blank=True, null=True, choices=gender_choice)



    def __str__(self):
        return str(self.author)
    
    def get_absolute_url(self):
        return reverse('user_profile', kwargs={'author': self.author})


def save_profile(sender, **kwargs):
    if kwargs['created']:
        p = Profile(author = kwargs['instance'])
        p.slug = slugify(p.author)
        p.email = User.objects.get(username = p.author).email
        p.save()    

post_save.connect(save_profile , sender=settings.AUTH_USER_MODEL)


class Post(models.Model):
    author = models.ForeignKey(settings.AUTH_USER_MODEL, blank=True, null=True, on_delete=models.CASCADE)
    slug = models.SlugField(unique=True, blank=True)
    title = models.CharField(max_length = 200)
    image = models.FileField(null=True, blank=True)
    content = models.TextField()
    category = models.ForeignKey(Category, verbose_name="Category",on_delete=models.CASCADE, null=True)
    profile = models.ForeignKey(Profile, verbose_name="Profile",on_delete=models.CASCADE,null=True)
    draft = models.BooleanField(default=False)
    publish = models.DateField(auto_now=False, auto_now_add=False)
    timestamp = models.DateTimeField(auto_now = False, auto_now_add= True,blank=True,null=True)
    updated = models.DateTimeField(auto_now = True, auto_now_add= False,blank=True,null=True)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('post_detail', kwargs={'slug': self.slug})
    

def create_slug(instance, new_slug=None):
    slug = slugify(instance.title)
    if new_slug is not None:
        slug=new_slug
    qs = Post.objects.filter(slug=slug).order_by("-id")
    exists = qs.exists()
    if exists:
        new_slug = "%s-%s" % (slug, qs.first().id)
        return create_slug(instance, new_slug=new_slug)
    return slug
    
def pre_save_post_reciever(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = create_slug(instance)

pre_save.connect(pre_save_post_reciever, sender=Post)


class Controlpanel(models.Model):
    profile_name=models.CharField(max_length=255,blank=True)
    favicon = models.FileField(null=True, blank=True)
    logo = models.FileField(null=True, blank=True)
    logo_width = models.IntegerField(blank=True)


    def __str__(self):
        return self.profile_name