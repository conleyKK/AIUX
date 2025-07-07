from django.contrib import admin
from .models import Category, DesignPattern, PatternFile


class PatternFileInline(admin.TabularInline):
    model = PatternFile
    extra = 0


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'description', 'created_at']
    search_fields = ['name']
    list_filter = ['created_at']


@admin.register(DesignPattern)
class DesignPatternAdmin(admin.ModelAdmin):
    list_display = ['title', 'category', 'is_featured', 'created_at']
    list_filter = ['category', 'is_featured', 'created_at']
    search_fields = ['title', 'description']
    inlines = [PatternFileInline]
    fieldsets = (
        ('基本信息', {
            'fields': ('title', 'category', 'description', 'cover_image')
        }),
        ('内容', {
            'fields': ('content',)
        }),
        ('其他设置', {
            'fields': ('tags', 'is_featured')
        }),
    )


@admin.register(PatternFile)
class PatternFileAdmin(admin.ModelAdmin):
    list_display = ['name', 'pattern', 'uploaded_at']
    list_filter = ['uploaded_at']
    search_fields = ['name', 'pattern__title']
