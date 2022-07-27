from django import forms
from django.contrib.auth.models import User
from .models import UserProfile
from django.contrib.auth.forms import PasswordChangeForm
from bootstrap_datepicker_plus import DatePickerInput
from blog import settings


class UserLoginForm(forms.Form):
    username = forms.CharField(label='İstifadəçi adı', max_length=50,
                               widget=forms.TextInput(attrs={'class': 'form-control'}))
    password = forms.CharField(label='Şifrə', max_length=50, widget=forms.PasswordInput(
        attrs={'class': 'form-control'}))

    def clean_username(self):
        username = self.cleaned_data['username']

        if '@' in username:
            user = User.objects.filter(email=username)

            if len(user) == 1:
                user = user.first()
                return user
            elif len(user) > 1:
                raise forms.ValidationError(
                    'Zəhmət olmasa istifadəçi adı ilə daxil olun')
            else:
                raise forms.ValidationError('Belə istifadəçi tapılmadı')
        return username


class UserRegisterForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(UserRegisterForm, self).__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs = {"class": "form-control"}
        self.fields[field].widget = forms.PasswordInput(
            attrs={"class": "form-control"})
        self.fields['username'].help_text = ''

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username', 'password']


class UserProfileForm(forms.ModelForm):
    KISI = 'K'
    QADIN = 'Q'
    BASQA = 'O'

    SECIM = ((KISI, 'Kişi'), (QADIN, 'Qadın'), (BASQA, 'Başqa'))

    cinsiyyet = forms.CharField(widget=forms.Select(choices=SECIM))
    telefon = forms.CharField(max_length=11, label='Telefon')
    bio = forms.CharField(widget=forms.Textarea,
                          max_length=500, label='Hakkında')
    brithday = forms.DateField(input_formats=['%d.%m.%Y'], widget=DatePickerInput(
        options={'format': "DD.MM.YYYY", 'viewMode': 'years'}))

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username',
                  'email', 'cinsiyyet', 'telefon', 'bio', 'brithday']

    def __init__(self, *args, **kwargs):
        super(UserProfileForm, self).__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs = {'class': 'form-control'}
            self.fields[field].help_text = ''


class UserProfileForm_UserProfile(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['cinsiyyet', 'telefon', 'bio', 'brithday']


class UserProfilePhotoEditForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['photo']


class UserChangePasswordForm(PasswordChangeForm):
    def __init__(self, *args, **kwargs):
        super(UserChangePasswordForm, self).__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs = {'class': 'form-control'}


class UserProfileVisibleForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(UserProfileVisibleForm, self).__init__(*args, **kwargs)
        self.fields['visible'].label = ''
        self.fields['visible'].widget.attrs = {'class': 'form-control'}


    class Meta:
        model = UserProfile
        fields = ['visible']
