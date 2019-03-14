from django.urls import path
from . import views

app_name = 'official'
urlpatterns = [
    path('', views.index, name='index'),
    path('forecas/', views.forecas, name='forecas'),                            # 点赞处理路径
    path('lev_message/<int:item_id>', views.lev_message, name='lev_message'),   # 发表动态处理路径
    path('see_msg/<int:item_id>', views.see_msg, name='see_msg'),               # 查看评论
    path('set_info/<int:items>', views.set_info, name='set_info'),              # 个人主页
    path('about_me/', views.about_me, name='about_me'),                         # 个人信息主页
]