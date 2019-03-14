from django.db import models
from django.utils.html import SafeText

# Create your models here.


class Category(models.Model):
    petName = models.CharField(max_length=16, verbose_name='宠物类别')

    def listKeyword(self):
        objs = self.keyword_set.all()
        arr = []
        for obj in objs:
            arr.append("<e style='margin:0 8px;color:#ff6700;font-size:14px'>"+obj.name+"<e>")
        return SafeText(''.join(arr))
    listKeyword.short_description = "关键字"

    class Meta:
        verbose_name = '分类'
        verbose_name_plural = '分类管理'

    def __str__(self):
        return self.petName


class Keyword(models.Model):
    name = models.CharField(max_length=20, verbose_name='宠物类别的关键字')
    c = models.ForeignKey(to=Category, on_delete=models.CASCADE)

    def __str__(self):
        return self.name



