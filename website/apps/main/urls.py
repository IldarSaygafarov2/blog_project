from django.urls import path
from . import views

urlpatterns = [
    path('', views.show_home_page, name='home-page'),
    path('contacts/', views.show_contacts_page, name='contacts-page'),
    path('faq/', views.show_faq_page, name='faq-page'),
    path('categories/<int:category_id>/', views.show_category_page, name='category-page'),
    path('articles/<int:article_id>/', views.show_article_detail_page, name='article-page'),
    path('articles/<int:article_id>/delete/', views.DeleteArticleView.as_view(), name='delete-article'),
    path('articles/<int:article_id>/update/', views.UpdateArticleView.as_view(), name='update-article'),
    path('articles/<int:article_id>/<str:action>/', views.add_like_or_dislike, name='vote'),
    path('create/', views.create_article_page, name='create-article'),
    path('articles/<int:article_id>/comments/<int:comment_id>/delete/', views.delete_comment, name='delete-comment'),
    path('search/', views.search_articles, name='search')
]