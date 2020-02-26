from django.conf.urls.static import static
from django.urls import path,include
from django.conf import settings
from . import views


urlpatterns = [
    path('', views.post_list, name="postlist"),
    path('post_detail/<slug:slug>/', views.post_detail, name="post_detail"),
    path('create/', views.post_create, name="post_create"),
    path('<slug:slug>/edit/', views.post_update, name = "post_update"),
    path('<int:id>/delete/', views.post_delete, name = "post_delete"),
    path('accounts/', include('registration.backends.default.urls')),
    path('c/<slug:category_slug>/', views.category_detail, name='category_detail'),
    path('accounts/<str:author>/profile/', views.user_profile, name='user_profile'),
    path('accounts/<slug:slug>/edit/', views.profile_edit, name='profile_edit'),
    path('<int:postid>/<int:commentid>/delete/', views.comment_delete, name="comment_delete"),
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

