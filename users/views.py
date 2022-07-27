from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.models import User
from django.http import JsonResponse
from django.template.loader import render_to_string
from django.contrib import messages
from django.urls import reverse
from . forms import *
from posts.models import Post
from following.models import Following

# Create your views here.


def user_register(request):
    form = UserRegisterForm(request.POST or None)

    if form.is_valid():

        username = form.cleaned_data['username']
        password = form.cleaned_data['password']
        new_user = form.save(commit=False)
        new_user.set_password(password)
        new_user.save()

        user = authenticate(username=username, password=password)
        if user:
            login(request, new_user)
            messages.success(request, 'Xoş gəldiniz - {}'.format(username))
            return redirect(reverse('index'))

    return render(request, 'users/register.html', context={'form': form})


def user_login(request):
    next = request.GET.get('next', '')
    form = UserLoginForm(request.POST or None)

    if request.user.is_authenticated:
        return redirect(reverse('index'))

    if form.is_valid():
        next = request.POST.get('next_t', '')
        username = form.cleaned_data['username']
        password = form.cleaned_data['password']
        user = authenticate(username=username, password=password)

        if user:
            login(request, user)
            if next != '':
                return redirect(next)
            messages.success(request, 'Xoş gəldiniz - {}'.format(username))

            return redirect(reverse('index'))
        else:
            messages.warning(request, 'İstifadəçi adı və ya şifrə yanlışdır')
            return render(request, 'users/login.html', context={'form': form, 'next': next})

    return render(request, 'users/login.html', context={'form': form, 'next': next})


@login_required(login_url='/users/login')
def user_logout(request):
    logout(request)
    messages.warning(request, 'Saytdan çıxış edildi..')
    return redirect(reverse('index'))


@login_required(login_url='/users/login')
def profile_edit(request):
    data = {
        'cinsiyyet': request.user.userprofile.cinsiyyet,
        'telefon': request.user.userprofile.telefon,
        'bio': request.user.userprofile.bio,
        'brithday': request.user.userprofile.brithday,
    }

    form = UserProfileForm(request.POST or None,
                           instance=request.user, initial=data)

    if form.is_valid():
        form.save()

        form2 = UserProfileForm_UserProfile(
            request.POST or None, instance=request.user.userprofile)
        form2.save(commit=True)

        messages.success(request, 'İstifadəçi məlumatları yeniləndi.')
        return redirect(reverse("dashboard", kwargs={'username': request.user}))

    return render(request, 'users/profile-edit.html', {'form': form})


@login_required(login_url='/users/login')
def dashboard(request, username):
    visible = True
    user = get_object_or_404(User, username=username)
    posts_count = Post.objects.all().filter(user=user).count()
    posts = Post.objects.all().filter(user=user)

    follow_status = False
    if user != request.user:
        follow_ship = Following.objects.filter(
            followed=user, follower=request.user)
        if follow_ship.exists():
            follow_status = True
            return render(request, 'users/dashboard.html', context={'posts': posts, 'user': user, 'visible': visible, 'posts_count': posts_count, 'follow_status': follow_status})

        if user.userprofile.visible == 'F':
            visible = False
    visible_form = UserProfileVisibleForm(instance=user.userprofile)
    return render(request, 'users/dashboard.html', context={'posts': posts, 'user': user, 'visible_form': visible_form, 'visible': visible, 'posts_count': posts_count})


@login_required(login_url='/users/login')
def password_edit(request):
    form = UserChangePasswordForm(request.user, request.POST or None)

    if form.is_valid():
        user = form.save()
        update_session_auth_hash(request, user)
        messages.success(request, 'Şifrə uğurla dəyişdirildi')
        return redirect('dashboard')
    context = {
        'form': form
    }
    return render(request, 'users/password-edit.html', context)


@login_required(login_url='/users/login')
def profile_photo_edit(request):
    if request.method == 'POST':
        form = UserProfilePhotoEditForm(
            instance=request.user.userprofile, data=request.POST, files=request.FILES)

        if form.is_valid():
            profile_photo = form.save(commit=True)
            return(JsonResponse(data={'is_valid': True, 'image_url': profile_photo.photo.url,
                                      'success': 'Photo edit'}))
        else:
            return(JsonResponse(data={'is_valid': False}))

    else:
        return redirect('dashboard')


def user_visible(request):
    data = {}
    if request.method == 'POST':
        profile = request.user.userprofile
        form = UserProfileVisibleForm(data=request.POST, instance=profile)
        form.save(commit=True)
        data = {'visible': profile.visible}
    return JsonResponse(data)


def user_followers(request,username):
    user = get_object_or_404(User,username=username)
    followers = user.followed.all()
    
    data = dict()

    if request.is_ajax():
        data['is_valid'] = True
        context = {'user':user,'followers':followers}

        data['html_followers_list']=render_to_string('users/includes/user_followers.html',context,request)

        return JsonResponse(data)
    return redirect(reverse('dashboard'),kwargs = {'username':user.username})


def user_followeds(request,username):
    user = get_object_or_404(User,username=username)
    followeds = user.follower.all()
    
    data = dict()

    if request.is_ajax():
        data['is_valid'] = True
        context = {'user':user,'followeds':followeds}

        data['html_followeds_list']=render_to_string('users/includes/user_followeds.html',context,request)

        return JsonResponse(data)
    return redirect(reverse('dashboard'),kwargs = {'username':user.username})