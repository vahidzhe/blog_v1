from django.shortcuts import render
from django.http import JsonResponse
from .models import Following, User


def add_or_delete_follow_view(request):
    followed = request.POST.get('followed', None)
    follower = request.POST.get('follower', None)

    followed = User.objects.filter(username=followed)
    follower = User.objects.filter(username=follower)


    if followed.exists() and follower.exists():
        followed = followed.first()
        follower = follower.first()
        data =  Following.add_or_delete_follow(followed=followed,follower=follower)
        return JsonResponse(data)
    return JsonResponse(data={'msg':'error'})