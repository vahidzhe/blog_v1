from django.db import models
from django.utils.text import slugify
from ckeditor.fields import RichTextField
from django.contrib.auth.models import User

def upload_to(instance,filename):
    return "{}/{}/{}".format('posts',instance.slug,filename)

# Create your models here.
class Category(models.Model):
    name = models.CharField(max_length=50,verbose_name='Kateqoriya')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Kateqoriya'
        verbose_name_plural = 'Kaetqoriyalar' 

class Post(models.Model):
    title = models.CharField(max_length=50,verbose_name='Başlığ',blank = False)
    user = models.ForeignKey(User,default=1,related_name='posts',on_delete = models.CASCADE,null=True)
    category = models.ManyToManyField(Category,verbose_name='Kateqoriya',related_name='post')

    slug = models.SlugField(max_length=122,default='',unique=True,null=False,verbose_name="Slug yeri",editable=False)
    content = RichTextField(verbose_name='Məzmun')
    image = models.ImageField(default = 'default.png',verbose_name="Şəkil",blank = True,upload_to = upload_to)
    draft = models.BooleanField(default=False)
    created_date = models.DateTimeField(auto_now_add=True)
    update_date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

    def unique_slug(self,new_slug,orjinal_slug,index):
        if Post.objects.filter(slug = new_slug):
            new_slug = "{}-{}".format(orjinal_slug,index)
            index += 1
            return self.unique_slug(new_slug=new_slug,orjinal_slug=orjinal_slug,index=index)
            
        return new_slug

    def save(self, *args, **kwargs):
        if self.slug == '':
            index = 1
            new_slug = slugify(self.title)
            self.slug = self.unique_slug(new_slug=new_slug,orjinal_slug=new_slug,index=index)
        super(Post, self).save(*args, **kwargs)

    class Meta:
        verbose_name = 'Məqalə'
        verbose_name_plural = 'Məqalələr'
        ordering = ['-created_date']


class Comment(models.Model):
    post = models.ForeignKey(Post,related_name='comment',verbose_name="Məqalə",on_delete = models.CASCADE)
    user = models.ForeignKey(User,default=1,on_delete = models.DO_NOTHING,related_name='comment')
    content = models.TextField(max_length=1000,verbose_name='Məzmun')
    created_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return 'Post - {} | User - {}'.format(self.post,self.user)

    class Meta:
        verbose_name = 'Şərh'
        verbose_name_plural = 'Şərhlər'

class ChildComment(models.Model):
    comment = models.ForeignKey(Comment,verbose_name='Şərh',related_name='child_comment',on_delete=models.CASCADE)
    user = models.ForeignKey(User,verbose_name='İstifadəçi',related_name='child_comment',on_delete=models.DO_NOTHING)
    content = models.TextField(max_length=500,verbose_name='Məzmun') 
    created_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return 'Comment ID-{}  |  User-{}'.format(self.comment.id,self.user)

    class Meta:
        verbose_name = 'İç-içə şərh'
        verbose_name_plural = 'İç-içə şərhlər'
        ordering = ['-created_date']
