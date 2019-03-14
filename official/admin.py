from django.contrib import admin
from .models import Category, Keyword

# Register your models here.

admin.AdminSite.site_title = '宠物平台管理系统'
admin.AdminSite.site_header = '旅行者Ⅰ号'
admin.AdminSite.index_title = '平台管理'


class KeywordInline(admin.StackedInline):
    model = Keyword
    extra = 3


@admin.register(Category)
class Category(admin.ModelAdmin):
    fields = ['petName']
    list_display = ['petName', 'listKeyword']
    inlines = [KeywordInline]






