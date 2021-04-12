from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.shortcuts import redirect, render, get_object_or_404
from .models import Post, Group, Follow
from .forms import PostForm, CommentForm


User = get_user_model()


def index(request):
    """Представление главной страницы"""
    post_list = Post.objects.all()
    paginator = Paginator(post_list, 10)
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)
    return render(request, 'index.html', {'page': page})


def group_posts(request, slug):
    """Представление главной страницы сообщества"""
    group = get_object_or_404(Group, slug=slug)
    posts = Post.objects.filter(group=group)
    paginator = Paginator(posts, 10)
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)
    return render(
        request,
        'group.html',
        {'group': group, 'page': page}
    )


@login_required
def new_post(request):
    """Представление формы нового поста"""
    form = PostForm(request.POST or None, files=request.FILES or None)
    if form.is_valid():
        post = form.save(commit=False)
        post.author = request.user
        form.save()
        return redirect('index')
    return render(request, 'post_form.html', {
        'form': form,
        'is_edit': False
    })


def profile(request, username):
    """Представление профайла пользователя"""
    author = User.objects.get(username=username)
    posts = Post.objects.filter(author=author)
    following = request.user.is_authenticated and Follow.objects.filter(
        user=request.user,
        author=author).exists()
    posts_quantity = posts.count()
    paginator = Paginator(posts, 10)
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)
    return render(request, 'profile.html', {
        'author': author,
        'page': page,
        'posts_quantity': posts_quantity,
        'following': following
    })


def post_view(request, username, post_id):
    """Представление страницы отдельного поста"""
    author = User.objects.get(username=username)
    form = CommentForm()
    post = get_object_or_404(Post, id=post_id)
    comments = post.comments.all()
    posts_quantity = Post.objects.filter(author=author).count()
    context = {
        'post': post,
        'author': author,
        'comments': comments,
        'posts_quantity': posts_quantity,
        'form': form
    }
    return render(request, 'post.html', context)


@login_required
def post_edit(request, username, post_id):
    """Представление формы редактирования поста"""
    post = get_object_or_404(Post, id=post_id)
    form = PostForm(instance=post)
    if post.author_id != request.user.id:
        return redirect('post', username, post_id)

    if request.method == 'POST':
        form = PostForm(
            request.POST or None,
            instance=post,
            files=request.FILES or None
        )
        if form.is_valid():
            form.save()
            return redirect('post', username, post_id)

    return render(request, 'post_form.html', {
        'form': form,
        'post': post,
        'is_edit': True
    })


@login_required
def add_comment(request, username, post_id):
    """Представление формы добавления комментария"""
    post = get_object_or_404(Post, id=post_id)
    form = CommentForm(request.POST or None)
    if form.is_valid():
        comment = form.save(commit=False)
        comment.post_id = post.id
        comment.author = request.user
        form.save()
    return redirect('post', request.user, post_id)


def page_not_found(request, exception):
    """Представление страницы ошибки 404"""
    return render(
        request,
        "misc/404.html",
        {"path": request.path},
        status=404
    )


def server_error(request):
    """Представление страницы ошибки 500"""
    return render(request, "misc/500.html", status=500)


@login_required
def follow_index(request):
    posts = Post.objects.filter(author__following__user=request.user)
    paginator = Paginator(posts, 10)
    page_number = request.GET.get("page")
    page = paginator.get_page(page_number)
    context = {
        "page": page,
        "paginator": paginator,
        "posts": posts,
    }
    return render(request, "follow.html", context)


@login_required
def profile_follow(request, username):
    user_to_follow = get_object_or_404(User, username=username)
    if request.user != user_to_follow:
        Follow.objects.get_or_create(user=request.user, author=user_to_follow)
    return redirect("profile", username=username)


@login_required
def profile_unfollow(request, username):
    user_to_unfollow = get_object_or_404(User, username=username)
    get_object_or_404(
        Follow,
        user=request.user,
        author=user_to_unfollow
    ).delete()
    return redirect('profile', username=username)
