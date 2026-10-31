from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.core.paginator import Paginator

from .models import Article
from .forms import ArticleForm, RegisterForm, CommentForm


# Главная страница
def home(request):
    articles = Article.objects.all()

    paginator = Paginator(articles, 5)

    page_number = request.GET.get('page')

    page_obj = paginator.get_page(page_number)

    return render(request, 'hello/home.html', {
        'page_obj': page_obj
    })


# Просмотр статьи
def article_detail(request, pk):

    article = get_object_or_404(Article, pk=pk)

    comments = article.comments.all().order_by('created_at')

    if request.method == 'POST':

        if not request.user.is_authenticated:
            return redirect('login')

        form = CommentForm(request.POST)

        if form.is_valid():

            comment = form.save(commit=False)

            comment.article = article
            comment.author = request.user

            comment.save()

            return redirect('article_detail', pk=pk)

    else:
        form = CommentForm()

    return render(request, 'hello/article_detail.html', {
        'article': article,
        'comments': comments,
        'form': form
    })


# Создание статьи
@login_required
def article_create(request):

    if request.method == 'POST':

        form = ArticleForm(request.POST)

        if form.is_valid():

            article = form.save(commit=False)

            article.author = request.user

            article.save()

            return redirect('home')

    else:
        form = ArticleForm()

    return render(request, 'hello/article_form.html', {
        'form': form,
        'title': 'Создание статьи'
    })


# Редактирование статьи
@login_required
def article_edit(request, pk):

    article = get_object_or_404(
        Article,
        pk=pk,
        author=request.user
    )

    if request.method == 'POST':

        form = ArticleForm(request.POST, instance=article)

        if form.is_valid():

            form.save()

            return redirect('article_detail', pk=pk)

    else:
        form = ArticleForm(instance=article)

    return render(request, 'hello/article_form.html', {
        'form': form,
        'title': 'Редактирование статьи'
    })


# Удаление статьи
@login_required
def article_delete(request, pk):

    article = get_object_or_404(
        Article,
        pk=pk,
        author=request.user
    )

    if request.method == 'POST':

        article.delete()

        return redirect('home')

    return render(request, 'hello/article_delete.html', {
        'article': article
    })


# Регистрация
def register(request):

    if request.method == 'POST':

        form = RegisterForm(request.POST)

        if form.is_valid():

            user = form.save()

            login(request, user)

            return redirect('home')

    else:
        form = RegisterForm()

    return render(request, 'hello/register.html', {
        'form': form
    })


# Авторизация
def user_login(request):

    if request.user.is_authenticated:
        return redirect('home')

    if request.method == 'POST':

        form = AuthenticationForm(
            request,
            data=request.POST
        )

        if form.is_valid():

            user = form.get_user()

            login(request, user)

            return redirect('home')

    else:
        form = AuthenticationForm()

    return render(request, 'hello/login.html', {
        'form': form
    })


# Выход
@login_required
def user_logout(request):

    if request.method == 'POST':
        logout(request)

    return redirect('home')
