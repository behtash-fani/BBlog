from django import forms
from .models import Post,Profile,Comments
from froala_editor.widgets import FroalaEditor




class PostForm(forms.ModelForm):
    publish = forms.DateField(widget = forms.SelectDateWidget)
    content = forms.CharField(widget=FroalaEditor)
    class Meta:
        model = Post
        fields = ['title','content', 'image','category','draft','publish']


class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['email','avatar','website','bio','gender']
    
class CommentForm(forms.ModelForm):
    class Meta:
        model = Comments
        fields = ['content',]