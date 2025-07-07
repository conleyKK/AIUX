from django.db import models

# Create your models here.

class HomePageIntro(models.Model):
    title = models.CharField(max_length=200, verbose_name='主标题')
    subtitle = models.CharField(max_length=300, blank=True, verbose_name='副标题')
    description = models.TextField(verbose_name='描述', blank=True)
    updated_at = models.DateTimeField(auto_now=True, verbose_name='更新时间')

    def __str__(self):
        return self.title or '首页介绍内容'
