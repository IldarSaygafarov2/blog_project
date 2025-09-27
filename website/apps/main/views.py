from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import Category, Article, Comment, Like, Dislike, ArticleViewCount
from .forms import ArticleForm, CommentForm
from django.views.generic import DeleteView, UpdateView
from django.core.paginator import Paginator


class UpdateArticleView(UpdateView):
    model = Article
    template_name = 'main/article_form.html'
    form_class = ArticleForm
    pk_url_kwarg = 'article_id'


# pk article_id
class DeleteArticleView(DeleteView):
    model = Article
    template_name = 'main/article_confirm_delete.html'  # название html файла, для потдверждения удаления
    success_url = '/'  # ссылка для перенаправления пользователя, после удаления
    pk_url_kwarg = 'article_id'


def show_home_page(request):
    # select * from main_category;
    # objects {%%}, {{}}

    articles = Article.objects.all()

    paginator = Paginator(articles, 3)  # [(1, [1,2,3])]
    page = request.GET.get('page')
    articles = paginator.get_page(page)

    context = {
        'articles': articles
    }
    return render(request, "main/index.html", context)


def show_contacts_page(request):
    return render(request, 'main/contacts.html')


def show_faq_page(request):
    return render(request, "main/faq.html")


def show_category_page(request, category_id):
    category = Category.objects.get(pk=category_id)  #
    articles = Article.objects.filter(category=category)

    paginator = Paginator(articles, 1)  # [(1, [1,2,3])]
    page = request.GET.get('page')
    articles = paginator.get_page(page)

    page_url = f'/categories/{category_id}/'

    context = {
        'category': category,
        'articles': articles,
        'page_url': page_url
    }
    return render(request, 'main/category_page.html', context)

# templatetags
# context_processor


def show_article_detail_page(request, article_id):
    article = Article.objects.get(id=article_id)

    try:
        article.likes
    except Exception as e:
        Like.objects.create(article=article)

    # создать новый объект для лайка
    # создать новый объект для дизлайка

    try:
        article.dislikes
    except Exception as e:
        Dislike.objects.create(article=article)

    if request.method == 'POST':
        form = CommentForm(data=request.POST)
        if form.is_valid():
            form = form.save(commit=False)
            form.author = request.user
            form.article = article
            form.save()
            return redirect('article-page', article.pk)
    else:
        form = CommentForm()

    # get_or_create
    if request.user.is_authenticated:
        article_viewed, created = ArticleViewCount.objects.get_or_create(article=article, user=request.user)

        if created:
            article.views += 1
            article.save()

    context = {
        'article': article,
        'form': form
    }
    return render(request, 'main/article_page.html', context)


def create_article_page(request):
    if request.method == 'POST':
        form = ArticleForm(data=request.POST, files=request.FILES)
        if form.is_valid():
            form = form.save(commit=False)
            form.author = request.user
            form.save()
            return redirect('article-page', form.pk)
    else:
        form = ArticleForm()

    context = {
        'form': form
    }
    return render(request, 'main/article_form.html', context)


# articles/{article_id}/comments/{comment_id}/delete

def delete_comment(request, article_id, comment_id):
    comment = Comment.objects.get(pk=comment_id)
    comment.delete()  # удаление комментария
    return redirect('article-page', article_id)


# action=add_like
# action=add_dislike

def add_like_or_dislike(request, article_id, action):
    article = Article.objects.get(id=article_id)

    if action == 'add_like':
        if request.user in article.likes.user.all():  # проверяем что пользователь уже добавил лайк для статьи
            article.likes.user.remove(request.user.pk)  # удаляем пользователя из списка тех кто добавил лайк
        else:
            article.likes.user.add(request.user.pk)
            article.dislikes.user.remove(request.user.pk)
    elif action == 'add_dislike':
        if request.user in article.dislikes.user.all():
            article.dislikes.user.remove(request.user.pk)
        else:
            article.dislikes.user.add(request.user.pk)
            article.likes.user.remove(request.user.pk)

    return redirect('article-page', article.pk)


def search_articles(request):
    # ?q=text
    search_query = request.GET.get('q')
    if search_query:
        articles = Article.objects.filter(title__iregex=search_query)
    else:
        articles = Article.objects.all()

    paginator = Paginator(articles, 3)  # [(1, [1,2,3])]
    page = request.GET.get('page')
    articles = paginator.get_page(page)

    context = {
        'articles': articles,
        'search_query': search_query
    }
    return render(request, 'main/search_page.html', context)