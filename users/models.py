from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
# Create your models here.


def upload_to(instance,filename):
    return "{}/{}/{}".format('user_profile',instance.user.username,filename)


class UserProfile(models.Model):
    KISI = 'K'
    QADIN = 'Q'
    BASQA = 'O'


    PUBLIC = 'P'
    FOLLOWING = 'F'

    VISIBLE = ((PUBLIC,'Public'),(FOLLOWING,'Following'))
    SECIM =  ((KISI,'Kişi'),(QADIN,'Qadın'),(BASQA,'Başqa'))

    user = models.OneToOneField(User,verbose_name='İstifadəçi adı',on_delete=models.CASCADE)
    telefon = models.CharField(max_length=11,verbose_name='Telefon',blank = True)
    cinsiyyet = models.CharField(verbose_name='Cinsiyyət',choices=SECIM,blank=True,max_length=1)
    visible = models.CharField(max_length=1,default=1,choices=VISIBLE)
    bio = models.TextField(max_length=500,blank=True,verbose_name='Hakkında')
    photo = models.ImageField(verbose_name="Şəkil",upload_to = upload_to,default = 'default_profile.png')
    brithday = models.DateField(verbose_name="Doğrum tarixi",blank=True, null=True)

    def __str__(self):
        return '{}  - Profili'.format(self.user)

    class Meta:
        verbose_name = 'Profil'
        verbose_name_plural = 'Profillər'

def create_user_profile(instance,created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)
post_save.connect(receiver = create_user_profile,sender = User)
    