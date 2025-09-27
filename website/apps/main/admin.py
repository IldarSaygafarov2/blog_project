from django.contrib import admin

from .models import Category, FAQ, Article, Comment, ArticleImage, ArticleViewCount


admin.site.register(ArticleViewCount)


class ArticleImageInline(admin.TabularInline):
    model = ArticleImage


class ArticleAdmin(admin.ModelAdmin):
    list_display = ['id', 'title', 'views', 'is_active', 'category', 'created_at']
    list_display_links = ['id', 'title']
    list_filter = ['created_at', 'category', 'is_active']
    search_fields = ['title']
    readonly_fields = ['views']
    list_editable = ['is_active', 'category']
    inlines = [ArticleImageInline]



admin.site.register(Category)  # Это регистрация новой таблицы в базе данных
admin.site.register(FAQ)
admin.site.register(Comment)
admin.site.register(Article, ArticleAdmin)
