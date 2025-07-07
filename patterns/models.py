from django.db import models
from django.utils import timezone
import json


class Category(models.Model):
    """设计模式分类"""
    name = models.CharField(max_length=100, verbose_name='分类名称')
    description = models.TextField(blank=True, verbose_name='分类描述')
    created_at = models.DateTimeField(default=timezone.now, verbose_name='创建时间')
    
    class Meta:
        verbose_name = '分类'
        verbose_name_plural = '分类'
        ordering = ['created_at']
    
    def __str__(self):
        return self.name


class DesignPattern(models.Model):
    """设计模式"""
    title = models.CharField(max_length=200, verbose_name='模式标题')
    description = models.TextField(verbose_name='模式描述')
    content = models.TextField(verbose_name='详细内容')  # 存储HTML内容
    cover_image = models.ImageField(upload_to='covers/', blank=True, null=True, verbose_name='封面图片')
    category = models.ForeignKey(Category, on_delete=models.CASCADE, verbose_name='所属分类')
    tags = models.CharField(max_length=200, blank=True, verbose_name='标签（用逗号分隔）')
    created_at = models.DateTimeField(default=timezone.now, verbose_name='创建时间')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='更新时间')
    is_featured = models.BooleanField(default=False, verbose_name='是否推荐')
    
    class Meta:
        verbose_name = '设计模式'
        verbose_name_plural = '设计模式'
        ordering = ['-created_at']
    
    def __str__(self):
        return self.title
    
    def get_tags_list(self):
        """获取标签列表"""
        if self.tags:
            return [tag.strip() for tag in self.tags.split(',') if tag.strip()]
        return []
    
    def get_content_html(self):
        """获取HTML格式的内容"""
        return self.content


class PatternFile(models.Model):
    """模式相关文件"""
    pattern = models.ForeignKey(DesignPattern, on_delete=models.CASCADE, related_name='files', verbose_name='所属模式')
    name = models.CharField(max_length=200, verbose_name='文件名称')
    file = models.FileField(upload_to='pattern_files/', verbose_name='文件')
    description = models.TextField(blank=True, verbose_name='文件描述')
    uploaded_at = models.DateTimeField(default=timezone.now, verbose_name='上传时间')
    
    class Meta:
        verbose_name = '模式文件'
        verbose_name_plural = '模式文件'
        ordering = ['uploaded_at']
    
    def __str__(self):
        return f"{self.pattern.title} - {self.name}"
