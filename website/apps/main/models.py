from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse

# Create your models here.


# main_categories
class Category(models.Model):
    name = models.CharField(max_length=60)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Категория'  # единственное число
        verbose_name_plural = 'Категории'  # множественное число


# python manage.py makemigrations

# сделать таблицу для вопросов ответов
# question - CharField
# answer - TextField


class FAQ(models.Model):
    question = models.CharField(max_length=100, verbose_name='Вопрос')
    answer = models.TextField(verbose_name='Ответ')

    def __str__(self):
        return self.question

    class Meta:
        verbose_name = 'Вопрос-ответ'
        verbose_name_plural = 'Вопросы-ответы'


# tabnine


# title
# short_description
# full_description
# views
# created_at
# updated_at
# image
# is_active
# category
# author

# media/articles/previews/
class Article(models.Model):
    title = models.CharField(max_length=120, verbose_name='Заголовок')
    short_description = models.TextField(max_length=300, verbose_name='Краткое описание', null=True, blank=True)
    full_description = models.TextField(verbose_name='Полное описание')
    views = models.IntegerField(default=0, verbose_name='Кол-во просмотров')
    is_active = models.BooleanField(default=True, verbose_name='Активна ли статья?')
    image = models.ImageField(upload_to='articles/previews/', verbose_name='Заставка', blank=True, null=True)
    created_at = models.DateTimeField(verbose_name='Дата создания', auto_now_add=True)
    updated_at = models.DateTimeField(verbose_name='Дата обновления', auto_now=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, verbose_name='Категория')
    author = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Пользователь')

    def get_absolute_url(self):
        return reverse('article-page', kwargs={'article_id': self.pk})

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Статья'
        verbose_name_plural = 'Статьи'

# отобразить данную модель в админ панели

# создать модель Comment
# text models.TextField
# author models.ForeignKey
# created_at models.DateTimeField

# добавить строковое представление
# зарегистрировать модель в админ панели


class Comment(models.Model):
    text = models.TextField(verbose_name='Комментарий')
    author = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Пользователь')
    article = models.ForeignKey(Article, on_delete=models.CASCADE, verbose_name='Статья', null=True)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')

    def __str__(self):
        return f'{self.author.username}: {self.text[:30]}...'

    class Meta:
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'


def make_article_image_path(instance, filename):
    return f'articles/images/{instance.article.pk}/{filename}'


class ArticleImage(models.Model):
    image = models.ImageField(upload_to=make_article_image_path, verbose_name='Фото')
    article = models.ForeignKey(Article, on_delete=models.CASCADE, verbose_name='Статья')

# OneToOneField
# ManyToManyField

# python manage.py makemigrations
# python manage.py migrate


class Like(models.Model):
    article = models.OneToOneField(Article, on_delete=models.CASCADE, related_name='likes', null=True)
    user = models.ManyToManyField(User, related_name='likes')


class Dislike(models.Model):
    article = models.OneToOneField(Article, on_delete=models.CASCADE, related_name='dislikes', null=True)
    user = models.ManyToManyField(User, related_name='dislikes')


# Like - Article 1

class ArticleViewCount(models.Model):
    article = models.ForeignKey(Article, on_delete=models.CASCADE, related_name='article_views')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='article_views', null=True)
