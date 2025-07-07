from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from .models import Category, DesignPattern
from admin_panel.models import HomePageIntro


def index(request):
    """首页视图"""
    categories = Category.objects.all()
    patterns = DesignPattern.objects.all()
    
    # 获取搜索参数
    search = request.GET.get('search')
    if search:
        patterns = patterns.filter(
            title__icontains=search
        ) | patterns.filter(
            description__icontains=search
        ) | patterns.filter(
            tags__icontains=search
        )
    
    # 获取分类筛选参数
    category_id = request.GET.get('category')
    if category_id:
        try:
            patterns = patterns.filter(category_id=category_id)
        except ValueError:
            pass
    
    intro = HomePageIntro.objects.first()
    
    context = {
        'categories': categories,
        'patterns': patterns,
        'selected_category': category_id,
        'search': search,
        'intro': intro,
    }
    return render(request, 'patterns/index.html', context)


def pattern_detail(request, pattern_id):
    """模式详情视图"""
    pattern = get_object_or_404(DesignPattern, id=pattern_id)
    context = {
        'pattern': pattern,
    }
    return render(request, 'patterns/detail.html', context)


def api_patterns(request):
    """API接口：获取模式列表"""
    category_id = request.GET.get('category')
    patterns = DesignPattern.objects.all()
    
    if category_id:
        try:
            patterns = patterns.filter(category_id=category_id)
        except ValueError:
            pass
    
    patterns_data = []
    for pattern in patterns:
        patterns_data.append({
            'id': pattern.id,
            'title': pattern.title,
            'description': pattern.description,
            'cover_image': pattern.cover_image.url if pattern.cover_image else '',
            'category': pattern.category.name,
            'tags': pattern.get_tags_list(),
            'created_at': pattern.created_at.strftime('%Y/%m/%d'),
            'is_featured': pattern.is_featured,
        })
    
    return JsonResponse({
        'patterns': patterns_data
    })
