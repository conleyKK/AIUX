from django.core.management.base import BaseCommand
from patterns.models import Category, DesignPattern


class Command(BaseCommand):
    help = '创建AI UX设计模式的演示数据'

    def handle(self, *args, **options):
        self.stdout.write('开始创建演示数据...')

        # 创建分类
        categories_data = [
            {
                'name': '对话界面',
                'description': 'AI聊天机器人、语音助手等对话式交互界面设计模式'
            },
            {
                'name': '智能推荐',
                'description': '基于AI算法的个性化推荐系统界面设计'
            },
            {
                'name': '数据可视化',
                'description': 'AI驱动的数据分析和可视化界面设计'
            },
            {
                'name': '自动化流程',
                'description': '智能工作流和自动化任务的用户界面设计'
            },
            {
                'name': '预测分析',
                'description': 'AI预测和分析结果的展示界面设计'
            }
        ]

        categories = {}
        for cat_data in categories_data:
            category, created = Category.objects.get_or_create(
                name=cat_data['name'],
                defaults={'description': cat_data['description']}
            )
            categories[cat_data['name']] = category
            if created:
                self.stdout.write(f'创建分类: {category.name}')

        # 创建设计模式
        patterns_data = [
            {
                'title': '智能对话气泡',
                'description': '为AI聊天机器人设计的智能对话气泡，支持多种消息类型和情感表达',
                'category': '对话界面',
                'tags': '聊天,AI,对话,气泡',
                'is_featured': True,
                'content': '''
                <h2>设计概述</h2>
                <p>智能对话气泡是现代AI聊天界面的核心组件，它不仅要传达信息，还要体现AI的智能性和人性化。</p>
                
                <h3>设计原则</h3>
                <ul>
                    <li><strong>清晰性</strong>：信息层次分明，易于理解</li>
                    <li><strong>一致性</strong>：保持统一的视觉风格</li>
                    <li><strong>反馈性</strong>：提供及时的状态反馈</li>
                    <li><strong>适应性</strong>：支持不同类型的内容</li>
                </ul>
                
                <h3>应用场景</h3>
                <p>适用于客服机器人、智能助手、教育AI等各种对话式AI产品。</p>
                '''
            },
            {
                'title': '个性化推荐卡片',
                'description': '基于用户行为和偏好的智能推荐卡片设计，提升用户参与度',
                'category': '智能推荐',
                'tags': '推荐,个性化,卡片,算法',
                'is_featured': True,
                'content': '''
                <h2>设计理念</h2>
                <p>个性化推荐卡片通过AI算法分析用户行为，为每个用户提供定制化的内容推荐。</p>
                
                <h3>核心特性</h3>
                <ul>
                    <li>动态内容适配</li>
                    <li>智能排序算法</li>
                    <li>用户反馈机制</li>
                    <li>A/B测试支持</li>
                </ul>
                '''
            },
            {
                'title': 'AI数据仪表板',
                'description': '展示AI分析结果的智能仪表板，支持实时数据更新和交互式探索',
                'category': '数据可视化',
                'tags': '仪表板,数据,可视化,实时',
                'is_featured': False,
                'content': '''
                <h2>功能特点</h2>
                <p>AI数据仪表板将复杂的数据分析结果以直观的方式呈现给用户。</p>
                
                <h3>设计要点</h3>
                <ul>
                    <li>信息架构清晰</li>
                    <li>视觉层次分明</li>
                    <li>交互反馈及时</li>
                    <li>响应式布局</li>
                </ul>
                '''
            },
            {
                'title': '智能工作流界面',
                'description': '自动化工作流程的用户界面设计，让复杂的AI流程变得简单易懂',
                'category': '自动化流程',
                'tags': '工作流,自动化,流程,界面',
                'is_featured': False,
                'content': '''
                <h2>设计目标</h2>
                <p>简化复杂的AI工作流程，让用户能够轻松理解和操作自动化任务。</p>
                
                <h3>关键元素</h3>
                <ul>
                    <li>流程可视化</li>
                    <li>状态指示器</li>
                    <li>错误处理</li>
                    <li>进度反馈</li>
                </ul>
                '''
            },
            {
                'title': 'AI预测结果展示',
                'description': '展示AI预测和分析结果的界面设计，包含置信度和解释性信息',
                'category': '预测分析',
                'tags': '预测,分析,结果,置信度',
                'is_featured': True,
                'content': '''
                <h2>设计挑战</h2>
                <p>如何将复杂的AI预测结果以用户能理解的方式呈现，是这个设计模式的核心挑战。</p>
                
                <h3>解决方案</h3>
                <ul>
                    <li>可视化置信度</li>
                    <li>提供解释信息</li>
                    <li>支持深入探索</li>
                    <li>历史对比功能</li>
                </ul>
                '''
            },
            {
                'title': '语音交互界面',
                'description': '为语音AI助手设计的交互界面，支持语音输入和多模态反馈',
                'category': '对话界面',
                'tags': '语音,交互,助手,多模态',
                'is_featured': False,
                'content': '''
                <h2>设计考虑</h2>
                <p>语音交互界面需要考虑听觉、视觉和触觉多种感官的协调配合。</p>
                
                <h3>设计要素</h3>
                <ul>
                    <li>语音状态指示</li>
                    <li>实时语音识别</li>
                    <li>多模态反馈</li>
                    <li>错误恢复机制</li>
                </ul>
                '''
            }
        ]

        for pattern_data in patterns_data:
            category = categories[pattern_data['category']]
            pattern, created = DesignPattern.objects.get_or_create(
                title=pattern_data['title'],
                defaults={
                    'description': pattern_data['description'],
                    'category': category,
                    'tags': pattern_data['tags'],
                    'is_featured': pattern_data['is_featured'],
                    'content': pattern_data['content']
                }
            )
            if created:
                self.stdout.write(f'创建设计模式: {pattern.title}')

        self.stdout.write(
            self.style.SUCCESS(
                f'演示数据创建完成！\n'
                f'- 创建了 {len(categories_data)} 个分类\n'
                f'- 创建了 {len(patterns_data)} 个设计模式'
            )
        ) 