from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from django.http import JsonResponse
from django.core.paginator import Paginator
from patterns.models import Category, DesignPattern, PatternFile
from django.contrib.auth import authenticate, login, logout
from django.views.decorators.csrf import csrf_exempt
import json
from django.http import HttpResponse
import os
from .models import HomePageIntro
from django.utils.safestring import mark_safe


def is_staff(user):
    return user.is_staff


def admin_login(request):
    """管理员登录页面"""
    if request.user.is_authenticated and request.user.is_staff:
        return redirect('admin_panel:dashboard')
    
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        
        if user and user.is_staff:
            login(request, user)
            return redirect('admin_panel:dashboard')
        else:
            messages.error(request, '用户名或密码错误，或您没有管理权限')
    
    return render(request, 'admin_panel/login.html')


@login_required
@user_passes_test(is_staff)
def admin_logout(request):
    """管理员登出"""
    logout(request)
    return redirect('admin_panel:login')


@login_required
@user_passes_test(is_staff)
def dashboard(request):
    """管理面板首页"""
    # 统计数据
    total_patterns = DesignPattern.objects.count()
    total_categories = Category.objects.count()
    featured_patterns = DesignPattern.objects.filter(is_featured=True).count()
    recent_patterns = DesignPattern.objects.order_by('-created_at')[:5]
    
    context = {
        'total_patterns': total_patterns,
        'total_categories': total_categories,
        'featured_patterns': featured_patterns,
        'recent_patterns': recent_patterns,
    }
    return render(request, 'admin_panel/dashboard.html', context)


@login_required
@user_passes_test(is_staff)
def pattern_list(request):
    """模式列表"""
    patterns = DesignPattern.objects.all().order_by('-created_at')
    
    # 搜索
    search = request.GET.get('search', '').strip()
    if search and search != 'None':
        patterns = patterns.filter(
            title__icontains=search
        ) | patterns.filter(
            description__icontains=search
        ) | patterns.filter(
            tags__icontains=search
        )
    
    # 分类筛选
    category_id = request.GET.get('category', '').strip()
    if category_id and category_id != 'None':
        try:
            patterns = patterns.filter(category_id=category_id)
        except ValueError:
            pass
    
    # 分页
    paginator = Paginator(patterns, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    categories = Category.objects.all()
    
    context = {
        'page_obj': page_obj,
        'categories': categories,
        'search': search if search != 'None' else '',
        'selected_category': category_id if category_id != 'None' else '',
    }
    return render(request, 'admin_panel/pattern_list.html', context)


@login_required
@user_passes_test(is_staff)
def pattern_create(request):
    """创建模式"""
    if request.method == 'POST':
        title = request.POST.get('title')
        description = request.POST.get('description')
        content = request.POST.get('content', '')  # 直接获取HTML内容
        category_id = request.POST.get('category')
        tags = request.POST.get('tags', '')
        is_featured = request.POST.get('is_featured') == 'on'
        cover_image = request.FILES.get('cover_image')
        
        try:
            category = Category.objects.get(id=category_id)
            pattern = DesignPattern.objects.create(
                title=title,
                description=description,
                content=content,  # 直接保存HTML内容
                category=category,
                tags=tags,
                is_featured=is_featured,
                cover_image=cover_image
            )
            messages.success(request, f'设计模式 "{pattern.title}" 创建成功！')
            return redirect('admin_panel:pattern_list')
        except Exception as e:
            messages.error(request, f'创建失败：{str(e)}')
    
    categories = Category.objects.all()
    return render(request, 'admin_panel/pattern_form.html', {
        'categories': categories,
        'action': 'create'
    })


@login_required
@user_passes_test(is_staff)
def pattern_edit(request, pattern_id):
    """编辑模式"""
    pattern = get_object_or_404(DesignPattern, id=pattern_id)
    
    if request.method == 'POST':
        pattern.title = request.POST.get('title')
        pattern.description = request.POST.get('description')
        pattern.content = request.POST.get('content', '')  # 直接获取HTML内容
        pattern.category_id = request.POST.get('category')
        pattern.tags = request.POST.get('tags', '')
        pattern.is_featured = request.POST.get('is_featured') == 'on'
        
        if request.FILES.get('cover_image'):
            pattern.cover_image = request.FILES.get('cover_image')
        
        try:
            pattern.save()
            messages.success(request, f'设计模式 "{pattern.title}" 更新成功！')
            return redirect('admin_panel:pattern_list')
        except Exception as e:
            messages.error(request, f'更新失败：{str(e)}')
    
    categories = Category.objects.all()
    return render(request, 'admin_panel/pattern_form.html', {
        'pattern': pattern,
        'categories': categories,
        'action': 'edit'
    })


@login_required
@user_passes_test(is_staff)
def pattern_delete(request, pattern_id):
    """删除模式"""
    pattern = get_object_or_404(DesignPattern, id=pattern_id)
    
    if request.method == 'POST':
        title = pattern.title
        pattern.delete()
        messages.success(request, f'设计模式 "{title}" 已删除')
        return redirect('admin_panel:pattern_list')
    
    return render(request, 'admin_panel/pattern_delete.html', {'pattern': pattern})


@login_required
@user_passes_test(is_staff)
def category_list(request):
    """分类列表"""
    categories = Category.objects.all().order_by('-created_at')
    
    # 搜索
    search = request.GET.get('search', '').strip()
    if search and search != 'None':
        categories = categories.filter(
            name__icontains=search
        ) | categories.filter(
            description__icontains=search
        )
    
    # 分页
    paginator = Paginator(categories, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'page_obj': page_obj,
        'search': search if search != 'None' else '',
    }
    return render(request, 'admin_panel/category_list.html', context)


@login_required
@user_passes_test(is_staff)
def category_create(request):
    """创建分类"""
    if request.method == 'POST':
        name = request.POST.get('name')
        description = request.POST.get('description', '')
        
        try:
            category = Category.objects.create(name=name, description=description)
            messages.success(request, f'分类 "{category.name}" 创建成功！')
            return redirect('admin_panel:category_list')
        except Exception as e:
            messages.error(request, f'创建失败：{str(e)}')
    
    return render(request, 'admin_panel/category_form.html', {'action': 'create'})


@login_required
@user_passes_test(is_staff)
def category_edit(request, category_id):
    """编辑分类"""
    category = get_object_or_404(Category, id=category_id)
    
    if request.method == 'POST':
        category.name = request.POST.get('name')
        category.description = request.POST.get('description', '')
        
        try:
            category.save()
            messages.success(request, f'分类 "{category.name}" 更新成功！')
            return redirect('admin_panel:category_list')
        except Exception as e:
            messages.error(request, f'更新失败：{str(e)}')
    
    return render(request, 'admin_panel/category_form.html', {
        'category': category,
        'action': 'edit'
    })


@login_required
@user_passes_test(is_staff)
def category_delete(request, category_id):
    """删除分类"""
    category = get_object_or_404(Category, id=category_id)
    
    if request.method == 'POST':
        name = category.name
        category.delete()
        messages.success(request, f'分类 "{name}" 已删除')
        return redirect('admin_panel:category_list')
    
    return render(request, 'admin_panel/category_delete.html', {'category': category})


def quill_test(request):
    """Quill编辑器测试页面"""
    html_content = '''<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Quill编辑器测试</title>
    <!-- Quill.js CSS -->
    <link href="https://cdn.quilljs.com/1.3.7/quill.snow.css" rel="stylesheet">
    <style>
        body {
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            max-width: 800px;
            margin: 0 auto;
            padding: 2rem;
            background: #f5f5f5;
        }
        
        .container {
            background: white;
            padding: 2rem;
            border-radius: 12px;
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        }
        
        h1 {
            color: #333;
            margin-bottom: 1.5rem;
            text-align: center;
        }
        
        .editor-container {
            border: 2px solid #e5e7eb;
            border-radius: 8px;
            background: white;
            margin-bottom: 1rem;
        }
        
        #quill-editor {
            min-height: 300px;
        }
        
        .ql-toolbar {
            border-top-left-radius: 6px;
            border-top-right-radius: 6px;
            border-bottom: 1px solid #e5e7eb;
        }
        
        .ql-container {
            border-bottom-left-radius: 6px;
            border-bottom-right-radius: 6px;
            font-size: 16px;
            line-height: 1.6;
        }
        
        .status {
            text-align: center;
            padding: 1rem;
            margin-bottom: 1rem;
            border-radius: 8px;
        }
        
        .status.success {
            background: #d1fae5;
            color: #065f46;
            border: 1px solid #a7f3d0;
        }
        
        .status.error {
            background: #fee2e2;
            color: #991b1b;
            border: 1px solid #fca5a5;
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>🖋️ Quill.js 富文本编辑器测试</h1>
        
        <div id="status" class="status">
            <span id="status-text">正在加载编辑器...</span>
        </div>
        
        <div class="editor-container">
            <div id="quill-editor"></div>
        </div>
    </div>

    <!-- Quill.js JavaScript -->
    <script src="https://cdn.quilljs.com/1.3.7/quill.min.js"></script>
    
    <script>
        document.addEventListener('DOMContentLoaded', function() {
            console.log('开始初始化Quill编辑器...');
            
            const statusEl = document.getElementById('status');
            const statusText = document.getElementById('status-text');
            
            try {
                // 检查Quill是否加载成功
                if (typeof Quill === 'undefined') {
                    throw new Error('Quill.js 未能正确加载');
                }
                
                // 初始化Quill编辑器
                const quill = new Quill('#quill-editor', {
                    theme: 'snow',
                    placeholder: '开始编写您的内容...',
                    modules: {
                        toolbar: [
                            [{ 'header': [1, 2, 3, 4, 5, 6, false] }],
                            ['bold', 'italic', 'underline', 'strike'],
                            [{ 'color': [] }, { 'background': [] }],
                            [{ 'list': 'ordered'}, { 'list': 'bullet' }],
                            [{ 'indent': '-1'}, { 'indent': '+1' }],
                            [{ 'align': [] }],
                            ['blockquote', 'code-block'],
                            ['link', 'image'],
                            ['clean']
                        ]
                    }
                });
                
                // 设置初始内容
                quill.setText('Quill编辑器测试成功！\\n\\n这是一个功能完整的富文本编辑器。\\n请尝试使用工具栏的各种功能！');
                
                // 显示成功状态
                statusEl.className = 'status success';
                statusText.innerHTML = '✅ Quill编辑器初始化成功！可以开始编辑了。';
                
                console.log('Quill编辑器初始化完成');
                
            } catch (error) {
                console.error('Quill编辑器初始化失败:', error);
                
                // 显示错误状态
                statusEl.className = 'status error';
                statusText.innerHTML = `❌ 编辑器初始化失败: ${error.message}`;
            }
        });
    </script>
</body>
</html>'''
    return HttpResponse(html_content, content_type='text/html')


@login_required
@user_passes_test(is_staff)
def intro_edit(request):
    """首页介绍内容编辑"""
    intro, _ = HomePageIntro.objects.get_or_create(id=1)
    if request.method == 'POST':
        intro.title = request.POST.get('title', '')
        intro.subtitle = request.POST.get('subtitle', '')
        intro.description = request.POST.get('description', '')
        intro.save()
        messages.success(request, '首页介绍内容已更新！')
        return redirect('admin_panel:intro_edit')
    return render(request, 'admin_panel/intro_form.html', {'intro': intro})
