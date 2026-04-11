from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.scrollview import ScrollView
from kivy.uix.progressbar import ProgressBar
from kivy.uix.image import Image
from kivy.graphics import Color, Rectangle
from kivy.clock import Clock
from data.game_data import game_data
from data.questions import QUESTIONS


class ReportScreen(Screen):
    """学习报告屏幕"""
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.build_ui()
        Clock.schedule_interval(self.update_report, 2)
    
    def build_ui(self):
        main_layout = BoxLayout(orientation='vertical', padding=15, spacing=10)
        
        # 顶部导航
        nav_bar = BoxLayout(size_hint_y=0.08, spacing=10)
        
        # 返回按钮（图标）
        back_box = BoxLayout(size_hint_x=0.12)
        back_icon = Image(source='assets/images/buttons/back.png', allow_stretch=True, keep_ratio=True)
        back_btn = Button(background_color=(0.6, 0.6, 0.6, 0.8), background_normal='')
        back_btn.bind(on_press=lambda x: self.go_back())
        back_box.add_widget(back_icon)
        back_box.add_widget(back_btn)
        nav_bar.add_widget(back_box)
        
        nav_bar.add_widget(Label(
            text='学习报告',
            font_size='22sp',
            color=(0.3, 0.7, 0.9, 1),
            bold=True,
            font_name='DefaultFont'
        ))
        
        main_layout.add_widget(nav_bar)
        
        # 内容滚动区
        scroll = ScrollView()
        content = BoxLayout(orientation='vertical', spacing=15, padding=10, size_hint_y=None)
        content.bind(minimum_height=content.setter('height'))
        
        # 总体统计卡片
        self.summary_card = self.create_summary_card()
        content.add_widget(self.summary_card)
        
        # 各科成绩卡片
        self.subjects_card = self.create_subjects_card()
        content.add_widget(self.subjects_card)
        
        # 学习趋势卡片
        self.trend_card = self.create_trend_card()
        content.add_widget(self.trend_card)
        
        # 成就进度卡片
        self.achievement_card = self.create_achievement_card()
        content.add_widget(self.achievement_card)
        
        scroll.add_widget(content)
        main_layout.add_widget(scroll)
        
        self.add_widget(main_layout)
    
    def create_summary_card(self):
        """创建总体统计卡片"""
        card = BoxLayout(orientation='vertical', size_hint_y=None, height=200, padding=15, spacing=10)
        
        # 背景色
        with card.canvas.before:
            Color(0.95, 0.97, 1, 1)
            card.rect = Rectangle(pos=card.pos, size=card.size)
        card.bind(pos=lambda obj, val: setattr(card.rect, 'pos', val))
        card.bind(size=lambda obj, val: setattr(card.rect, 'size', val))
        
        card.add_widget(Label(
            text='[统计] 学习概况',
            font_size='18sp',
            color=(0.3, 0.7, 0.9, 1),
            bold=True,
            font_name='DefaultFont',
            size_hint_y=0.2
        ))
        
        # 统计数据网格
        grid = GridLayout(cols=3, spacing=10, size_hint_y=0.8)
        
        self.stat_labels = {}
        stats = [
            ('total_questions', '答题总数', '[书]'),
            ('correct_rate', '正确率', '[靶]'),
            ('total_coins', '获得金币', '[金币]'),
            ('pig_level', '猪小弟等级', '[猪]'),
            ('study_days', '学习天数', '[日历]'),
            ('today_questions', '今日答题', '[今日]')
        ]
        
        for key, label, icon in stats:
            box = BoxLayout(orientation='vertical')
            box.add_widget(Label(
                text=f'{icon} {label}',
                font_size='12sp',
                color=(0.5, 0.5, 0.5, 1),
                font_name='DefaultFont'
            ))
            self.stat_labels[key] = Label(
                text='0',
                font_size='24sp',
                bold=True,
                color=(0.3, 0.7, 0.9, 1),
                font_name='DefaultFont'
            )
            box.add_widget(self.stat_labels[key])
            grid.add_widget(box)
        
        card.add_widget(grid)
        return card
    
    def create_subjects_card(self):
        """创建各科成绩卡片"""
        card = BoxLayout(orientation='vertical', size_hint_y=None, height=250, padding=15, spacing=10)
        
        with card.canvas.before:
            Color(1, 0.97, 0.95, 1)
            card.rect = Rectangle(pos=card.pos, size=card.size)
        card.bind(pos=lambda obj, val: setattr(card.rect, 'pos', val))
        card.bind(size=lambda obj, val: setattr(card.rect, 'size', val))
        
        card.add_widget(Label(
            text='[科目] 各科成绩',
            font_size='18sp',
            color=(0.95, 0.5, 0.3, 1),
            bold=True,
            font_name='DefaultFont',
            size_hint_y=0.15
        ))
        
        # 各科进度
        self.subject_bars = {}
        subjects = ['语文', '数学', '英语', '科学']
        colors = [(0.9, 0.4, 0.4, 1), (0.4, 0.7, 0.9, 1), (0.4, 0.9, 0.4, 1), (0.9, 0.7, 0.4, 1)]
        
        for subject, color in zip(subjects, colors):
            row = BoxLayout(size_hint_y=0.2, spacing=10)
            row.add_widget(Label(
                text=subject,
                font_size='14sp',
                size_hint_x=0.2,
                font_name='DefaultFont'
            ))
            
            bar_container = BoxLayout(size_hint_x=0.6)
            bar = ProgressBar(max=100, value=0)
            self.subject_bars[subject] = bar
            bar_container.add_widget(bar)
            row.add_widget(bar_container)
            
            self.subject_bars[f'{subject}_label'] = Label(
                text='0/100',
                font_size='12sp',
                size_hint_x=0.2,
                font_name='DefaultFont'
            )
            row.add_widget(self.subject_bars[f'{subject}_label'])
            
            card.add_widget(row)
        
        return card
    
    def create_trend_card(self):
        """创建学习趋势卡片"""
        card = BoxLayout(orientation='vertical', size_hint_y=None, height=150, padding=15, spacing=10)
        
        with card.canvas.before:
            Color(0.97, 1, 0.95, 1)
            card.rect = Rectangle(pos=card.pos, size=card.size)
        card.bind(pos=lambda obj, val: setattr(card.rect, 'pos', val))
        card.bind(size=lambda obj, val: setattr(card.rect, 'size', val))
        
        card.add_widget(Label(
            text='[趋势] 学习进度',
            font_size='18sp',
            color=(0.4, 0.8, 0.4, 1),
            bold=True,
            font_name='DefaultFont',
            size_hint_y=0.3
        ))
        
        # 进度条
        self.progress_bar = ProgressBar(max=400, value=0, size_hint_y=0.3)
        card.add_widget(self.progress_bar)
        
        self.progress_label = Label(
            text='已完成 0/400 题',
            font_size='14sp',
            color=(0.5, 0.5, 0.5, 1),
            font_name='DefaultFont',
            size_hint_y=0.4
        )
        card.add_widget(self.progress_label)
        
        return card
    
    def create_achievement_card(self):
        """创建成就进度卡片"""
        card = BoxLayout(orientation='vertical', size_hint_y=None, height=180, padding=15, spacing=10)
        
        with card.canvas.before:
            Color(1, 0.97, 0.9, 1)
            card.rect = Rectangle(pos=card.pos, size=card.size)
        card.bind(pos=lambda obj, val: setattr(card.rect, 'pos', val))
        card.bind(size=lambda obj, val: setattr(card.rect, 'size', val))
        
        card.add_widget(Label(
            text='[奖杯] 成就进度',
            font_size='18sp',
            color=(1, 0.84, 0, 1),
            bold=True,
            font_name='DefaultFont',
            size_hint_y=0.2
        ))
        
        # 成就统计
        self.achievement_grid = GridLayout(cols=2, spacing=10, size_hint_y=0.8)
        
        achievements = [
            ('初出茅庐', '完成第一次答题'),
            ('小学者', '答对10道题'),
            ('小学霸', '答对50道题'),
            ('知识达人', '答对100道题'),
            ('小猪饲养员', '猪小弟达到3级'),
            ('小富翁', '拥有500金币')
        ]
        
        self.achievement_labels = {}
        for name, desc in achievements:
            box = BoxLayout(orientation='vertical', size_hint_y=None, height=50)
            box.add_widget(Label(
                text=name,
                font_size='14sp',
                bold=True,
                color=(0.3, 0.3, 0.3, 1),
                font_name='DefaultFont'
            ))
            label = Label(
                text='未完成',
                font_size='11sp',
                color=(0.7, 0.7, 0.7, 1),
                font_name='DefaultFont'
            )
            self.achievement_labels[name] = label
            box.add_widget(label)
            self.achievement_grid.add_widget(box)
        
        card.add_widget(self.achievement_grid)
        return card
    
    def update_report(self, dt):
        """更新报告数据"""
        achievements = game_data.get_achievements()
        pig = game_data.get_pig_status()
        
        # 更新总体统计
        total = achievements.get('questions_answered', 0)
        correct = achievements.get('correct_answers', 0)
        rate = (correct / total * 100) if total > 0 else 0
        
        self.stat_labels['total_questions'].text = str(total)
        self.stat_labels['correct_rate'].text = f'{rate:.1f}%'
        self.stat_labels['total_coins'].text = str(game_data.get_coins())
        self.stat_labels['pig_level'].text = str(pig.get('level', 1))
        self.stat_labels['study_days'].text = str(achievements.get('days_played', 1))
        
        # 今日答题数
        daily_tasks = game_data.data.get('daily_tasks', {})
        today_q = daily_tasks.get('questions_today', 0)
        self.stat_labels['today_questions'].text = str(today_q)
        
        # 更新各科进度（按答题数计算）
        # 这里简化处理，实际应该记录各科答题数
        for subject in ['语文', '数学', '英语', '科学']:
            count = len(QUESTIONS.get(subject, []))
            # 假设平均分配答题数
            subject_answered = min(count, total // 4)
            progress = (subject_answered / count * 100) if count > 0 else 0
            
            self.subject_bars[subject].value = progress
            self.subject_bars[f'{subject}_label'].text = f'{subject_answered}/{count}'
        
        # 更新总体进度
        total_questions = sum(len(QUESTIONS.get(s, [])) for s in ['语文', '数学', '英语', '科学'])
        self.progress_bar.max = total_questions
        self.progress_bar.value = total
        self.progress_label.text = f'已完成 {total}/{total_questions} 题'
        
        # 更新成就状态
        self.update_achievements(achievements, pig)
    
    def update_achievements(self, achievements, pig):
        """更新成就状态"""
        total = achievements.get('questions_answered', 0)
        correct = achievements.get('correct_answers', 0)
        coins = game_data.get_coins()
        level = pig.get('level', 1)
        
        # 检查各成就
        checks = [
            ('初出茅庐', total >= 1),
            ('小学者', correct >= 10),
            ('小学霸', correct >= 50),
            ('知识达人', correct >= 100),
            ('小猪饲养员', level >= 3),
            ('小富翁', coins >= 500)
        ]
        
        for name, unlocked in checks:
            if unlocked:
                self.achievement_labels[name].text = '[对] 已解锁'
                self.achievement_labels[name].color = (0.4, 0.8, 0.4, 1)
    
    def go_back(self):
        """返回首页"""
        self.manager.current = 'home'
    
    def on_enter(self):
        """进入屏幕时更新"""
        self.update_report(0)
