from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from .forms import LoginForm, RegistrationForm
from django.contrib.auth.models import User
from apps.main.models import Like, Dislike


def login_user(request):
    # GET, POST
    if request.method == 'POST':
        form = LoginForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()  # получает пользователя с БД через отправленные значения из формы
            login(request, user)
            return redirect('home-page')
    else:
        form = LoginForm()

    context = {
        'form': form
    }
    return render(request, 'users/login.html', context)


def register_user(request):
    if request.method == 'POST':
        form = RegistrationForm(data=request.POST)
        if form.is_valid():
            form.save()  # form.save() - сохраняет данные пользователя БД
            return redirect('login-user')
    else:
        form = RegistrationForm()
    context = {
        'form': form
    }
    return render(request, 'users/registration.html', context)


def logout_user(request):
    logout(request)
    return redirect('home-page')


def profile_page(request, username):
    author = User.objects.get(username=username)
    author_articles = author.article_set.all()  # получили все статьи пользователя
    for article in author_articles:
        try:
            article.likes
        except Exception as e:
            Like.objects.create(article=article)

        try:
            article.dislikes
        except Exception as e:
            Dislike.objects.create(article=article)

    total_views = sum([article.views for article in author_articles])

    total_comments = sum([article.comment_set.all().count() for article in author_articles])

    total_likes = sum([article.likes.user.all().count() for article in author_articles])
    total_dislikes = sum([article.likes.user.all().count() for article in author_articles])

    context = {
        'author': author,
        'total_comments': total_comments,
        'total_likes': total_likes,
        'total_dislikes': total_dislikes,
        'total_views': total_views
    }
    return render(request, 'users/profile.html', context)

