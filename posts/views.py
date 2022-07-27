from django.shortcuts import render,redirect,HttpResponse,get_object_or_404,Http404
from django.db.models import Q
from django.urls import reverse
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from . models import Post,Comment,ChildComment
from . forms import PostForm,PostFilterForum,CommentForum
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from django.http import JsonResponse


# Create your views here.
def index(request):
    page = request.GET.get('page', 1)
    search = request.GET.get('q',None)
    posts = Post.objects.all()
    draft = PostFilterForum(request.GET or None)

    if search:
        posts = Post.objects.filter(Q(title__icontains = search) |Q(content__icontains = search) |Q(category__name__icontains = search))


    if draft.is_valid():
        value = draft.cleaned_data['secme']
        if value == 'T':
            posts = Post.objects.filter(draft = True)
        elif value == 'TO':
            posts = Post.objects.filter(draft = False)

    
    
    paginator = Paginator(posts, 4)
    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        post = paginator.page(1)
    except EmptyPage:
        post = paginator.page(paginator.num_pages)

    return render(request,"posts/post_list.html",context={'posts':posts,'draft':draft})

@login_required(login_url='/users/login')
def post_detail(request,slug):
    post = get_object_or_404(Post,slug = slug)
    form = CommentForum(request.POST or None)

    if form.is_valid():
        comment = form.save(commit=False)
        comment.user = request.user
        comment.post = post
        comment.save()
        
        messages.success(request,'Şərh əlavə edildi')
        return redirect(reverse('detail',kwargs={'slug':post.slug}))
    return render(request,'posts/post_detail.html',context={'post':post,'form':form})

@login_required(login_url='/users/login')
def add_child_comment(request,id):
    comment = get_object_or_404(Comment,id=id)
    if request.method == 'POST':
        user = request.user
        content = request.POST['child-text']
        
        ChildComment.objects.create(comment=comment,user=user,content=content)
        return redirect(reverse('detail',kwargs={'slug':comment.post.slug}))

@login_required(login_url='/users/login')
def post_create(request):
    # form = PostForm()
    # if request.method == "POST":
    form = PostForm(request.POST or None,request.FILES or None)
    if form.is_valid():
        created_post = form.save(commit=True)
        created_post.user = request.user
        created_post.save()

        messages.success(request,'Məqalə uğurla əlavə edildi.')
        return redirect(reverse('index'))
    return render(request,'posts/post_create.html',context={'form':form})


@login_required(login_url='/users/login')
def post_update(request,slug):
    post = get_object_or_404(Post,slug=slug)
    if request.user != post.user:
        return Http404()
    form = PostForm(request.POST or None,request.FILES or None, instance=post)
    if form.is_valid():
        form.save(commit=True)
        messages.success(request,'Məqalə redaktə edildi.')
        return redirect(reverse('index'))
    return render(request,'posts/post_update.html',context={'form':form})


@login_required(login_url='/users/login')
def post_delete(request,slug):

    post = get_object_or_404(Post,slug = slug)
    if request.user != post.user:
        return Http404()
    else:
        if request.method == 'POST':
            post.delete()
            
            return JsonResponse(data = {'success':'silindi'})
            

    
    return redirect(reverse('index'))
