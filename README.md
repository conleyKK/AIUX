# AI UX Design Patterns 网站

这是一个用于展示和管理AI UX设计模式的网站，使用Django框架开发，采用现代化的Tailwind CSS设计。

## 🎨 功能特性

- **🎯 现代化UI设计**: 使用Tailwind CSS构建的响应式界面，美观且易用
- **📱 响应式设计**: 完美适配桌面、平板和移动设备
- **🎨 模式展示**: 以精美卡片形式展示设计模式，包含封面图、标题、描述等
- **🏷️ 智能筛选**: 通过分类按钮快速筛选不同类型的设计模式
- **📝 富文本编辑**: 支持CKEditor富文本编辑器编写详细的模式介绍
- **📁 文件管理**: 支持上传和下载相关设计文件
- **🔧 自定义管理后台**: 基于Tailwind CSS的现代化管理界面
- **🔍 搜索功能**: 支持模式标题和分类的搜索筛选
- **📊 数据统计**: 管理面板提供详细的数据统计信息

## 🛠 技术栈

- **后端**: Django 4.2.7
- **数据库**: SQLite (可扩展为MySQL)
- **富文本编辑器**: CKEditor
- **前端框架**: Tailwind CSS 3.x
- **图标**: Font Awesome 6.0
- **JavaScript**: 原生ES6+

## 🚀 快速开始

### 1. 环境准备

```bash
# 克隆项目
git clone <repository-url>
cd aiux-design

# 创建虚拟环境
python3 -m venv venv
source venv/bin/activate  # Linux/Mac
# 或 venv\\Scripts\\activate  # Windows

# 安装依赖
pip install -r requirements.txt
```

### 2. 数据库设置

```bash
# 创建数据库迁移
python manage.py makemigrations

# 执行迁移
python manage.py migrate

# 创建超级用户
python manage.py createsuperuser
```

### 3. 启动服务

```bash
# 启动开发服务器
python manage.py runserver
```

## 🌐 访问地址

- **网站首页**: http://127.0.0.1:8000
- **自定义管理面板**: http://127.0.0.1:8000/admin/
- **Django原生管理**: http://127.0.0.1:8000/django-admin/

## 📖 使用说明

### 🔐 管理后台操作

1. **登录管理面板**:
   - 访问 `/admin/login/` 
   - 使用超级用户账号登录

2. **创建分类**:
   - 进入"分类管理"
   - 点击"新建分类"
   - 填写分类名称和描述

3. **创建设计模式**:
   - 进入"设计模式管理"
   - 点击"新建模式"
   - 填写基本信息：标题、分类、描述
   - 上传封面图片
   - 使用富文本编辑器编写详细内容
   - 设置标签（用逗号分隔）
   - 可选择是否为推荐模式

4. **管理功能**:
   - 搜索和筛选模式
   - 编辑现有模式
   - 删除模式（带确认提示）
   - 查看统计数据

### 🎯 前端功能

- **首页浏览**: 查看所有设计模式卡片，支持悬停动画效果
- **分类筛选**: 点击分类按钮筛选特定类型的模式
- **详情查看**: 点击卡片查看模式详细信息，包含侧边栏信息
- **文件下载**: 在详情页下载相关文件
- **响应式体验**: 在各种设备上都有良好的用户体验

## 📁 项目结构

```
aiux_design/
├── aiux_design/          # 项目配置
│   ├── settings.py       # Django设置
│   ├── urls.py          # 主URL配置
│   └── ...
├── patterns/            # 模式应用
│   ├── models.py        # 数据模型
│   ├── views.py         # 视图函数
│   ├── admin.py         # Django原生管理配置
│   └── urls.py          # URL配置
├── admin_panel/         # 自定义管理面板
│   ├── views.py         # 管理面板视图
│   └── urls.py          # 管理面板URL
├── templates/           # 模板文件
│   ├── base.html        # 前端基础模板
│   ├── patterns/        # 模式相关模板
│   └── admin_panel/     # 管理面板模板
├── static/              # 静态文件
│   ├── css/             # 样式文件
│   └── js/              # JavaScript文件
├── media/               # 媒体文件（上传的图片和文件）
└── requirements.txt     # 项目依赖
```

## 🎨 UI设计特色

### 前端界面
- **渐变背景**: Hero区域采用紫蓝渐变背景
- **卡片设计**: 现代化的卡片布局，支持悬停动画
- **响应式网格**: 自适应的网格布局系统
- **优雅的排版**: 清晰的层次结构和可读性

### 管理面板
- **侧边栏导航**: 固定侧边栏，清晰的导航结构
- **统计卡片**: 直观的数据展示卡片
- **表单设计**: 现代化的表单样式和验证
- **操作反馈**: 丰富的消息提示和确认对话框

## 📊 数据模型

### Category (分类)
- name: 分类名称
- description: 分类描述
- created_at: 创建时间

### DesignPattern (设计模式)
- title: 模式标题
- description: 模式描述
- content: 详细内容（富文本）
- cover_image: 封面图片
- category: 所属分类
- tags: 标签
- is_featured: 是否推荐
- created_at/updated_at: 创建/更新时间

### PatternFile (模式文件)
- pattern: 所属模式
- name: 文件名称
- file: 文件
- description: 文件描述
- uploaded_at: 上传时间

## 🔧 自定义和扩展

### 添加新功能
1. 在相应的 `models.py` 中添加新的数据模型
2. 在 `admin_panel/views.py` 中添加管理视图
3. 创建相应的模板文件
4. 更新URL配置

### 样式定制
- 项目使用Tailwind CSS，可通过修改类名来调整样式
- 自定义颜色和主题可在模板中的Tailwind配置中修改

### 数据库切换到MySQL
1. 安装MySQL客户端: `pip install mysqlclient`
2. 修改 `settings.py` 中的数据库配置
3. 重新执行迁移

## 🚀 部署建议

1. **生产环境设置**:
   - 设置 `DEBUG = False`
   - 配置 `ALLOWED_HOSTS`
   - 使用环境变量管理敏感信息

2. **静态文件处理**:
   ```bash
   python manage.py collectstatic
   ```

3. **Web服务器**: 推荐使用Nginx + Gunicorn

4. **CDN优化**: 可将Tailwind CSS和Font Awesome改为本地文件以提高加载速度

## 📄 许可证

MIT License

## 🤝 贡献

欢迎提交Issue和Pull Request来改进这个项目！

## 📞 支持

如果您在使用过程中遇到问题，请：
1. 查看项目文档
2. 搜索已有的Issues
3. 创建新的Issue描述问题 