from django import forms
from . models import Post,Comment

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title','category','content','image','draft']

    
    def __init__(self,*args,**kwargs):
        super(PostForm, self).__init__(*args,**kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs={"class":"form-control"}
        self.fields['draft'].widget.attrs={"class":""}
        self.fields['image'].widget.attrs={"class":""}

class PostFilterForum(forms.Form):
    SECME = (('H','Hamısı'),
            ('T','Taslaklı'),
            ('TO','Taslak olmayan'),
    )

    secme = forms.CharField(label='',widget=forms.Select(choices=SECME,attrs={'class':'form-control'}),required=None)
   
  
class CommentForum(forms.ModelForm):


    def __init__(self,*args,**kwargs):
        super(CommentForum, self).__init__(*args,**kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs={"class":"form-control"}

    class Meta:
        model = Comment
        fields = ['content']

    