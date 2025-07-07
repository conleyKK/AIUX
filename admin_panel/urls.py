from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

app_name = 'admin_panel'

urlpatterns = [
    # 登录登出
    path('login/', views.admin_login, name='login'),
    path('logout/', views.admin_logout, name='logout'),
    
    # 仪表板
    path('', views.dashboard, name='dashboard'),
    
    # 设计模式管理
    path('patterns/', views.pattern_list, name='pattern_list'),
    path('patterns/create/', views.pattern_create, name='pattern_create'),
    path('patterns/<int:pattern_id>/edit/', views.pattern_edit, name='pattern_edit'),
    path('patterns/<int:pattern_id>/delete/', views.pattern_delete, name='pattern_delete'),
    
    # 分类管理
    path('categories/', views.category_list, name='category_list'),
    path('categories/create/', views.category_create, name='category_create'),
    path('categories/<int:category_id>/edit/', views.category_edit, name='category_edit'),
    path('categories/<int:category_id>/delete/', views.category_delete, name='category_delete'),
    
    # 测试页面
    path('test-quill/', views.quill_test, name='quill_test'),
    
    # 修改密码
    path('password_change/', auth_views.PasswordChangeView.as_view(template_name='admin_panel/password_change_form.html'), name='password_change'),
    path('password_change/done/', auth_views.PasswordChangeDoneView.as_view(template_name='admin_panel/password_change_done.html'), name='password_change_done'),
    
    # 首页介绍内容编辑
    path('intro/', views.intro_edit, name='intro_edit'),
] 