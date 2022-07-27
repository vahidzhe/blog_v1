from django.db import models
from django.contrib.auth.models import User
# Create your models here.


class Following(models.Model):
    followed = models.ForeignKey(
        User, verbose_name='Takib edilen', on_delete = models.CASCADE, related_name='followed')
    follower = models.ForeignKey(
        User, verbose_name='Takib eden',on_delete = models.CASCADE, related_name='follower')

    def save(self,*args, **kwargs):
        if self.followed != self.follower:
            return super(Following, self).save(*args, **kwargs)

 
    def __str__(self):
        return '{} - {}'.format(self.followed,self.follower)

    @staticmethod
    def add_or_delete_follow(followed,follower):
        data = {}
        value = Following.objects.filter(followed=followed,follower=follower)
        if value.exists():
            value.delete()
            print(followed,follower)
            count = Following.get_followed_count(user=follower)
            data = {'msg':'Takib et','count':count}
            return data
        Following.objects.create(followed=followed,follower=follower)
        count = Following.get_followed_count(user=follower)
        data = {'msg':'Takib burax','count':count}
        return data
    
    class Meta:
        verbose_name = 'Takib'
        verbose_name_plural = 'Takiblər'

    @staticmethod
    def get_followed(user):
        takibciler = Following.objects.filter(follower = user)  #Useri takib edenler
        return takibciler

    @staticmethod
    def get_followed_count(user):
        takibciler_sayi = Following.objects.filter(follower = user).count()
        return takibciler_sayi

    @staticmethod
    def get_follower(user):
        takibler = Following.objects.filter(followed = user) #Userin takib etdikleri
        return takibler

    @staticmethod
    def get_follower_count(user):
        takibler_sayi = Following.objects.filter(followed = user).count()
        return takibler_sayi

    @staticmethod
    def user_takipcilerim_status(me,other):
        has_follow = Following.objects.filter(followed=other,follower=me).exists()
        return has_follow