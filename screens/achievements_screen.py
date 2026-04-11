from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.gridlayout import GridLayout
from kivy.uix.scrollview import ScrollView
from kivy.clock import Clock
from data.game_data import game_data


class AchievementsScreen(Screen):
    """成就屏幕"""
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.build_ui()
        Clock.schedule_interval(self.update_stats, 2)
    
    def build_ui(self):
        main_layout = BoxLayout(orientation='vertical', padding=15, spacing=10)
        
        # 顶部导航
        nav_bar = BoxLayout(size_hint_y=0.08, spacing=10)
        back_btn = Button(
            text='<- 返回',
            size_hint_x=0.2,
            background_color=(0.6, 0.6, 0.6, 1),
            font_name='DefaultFont'
        )
        back_btn.bind(on_press=lambda x: self.go_back())
        nav_bar.add_widget(back_btn)
        
        nav_bar.add_widget(Label(
            text='[奖杯] 学习成就',
            font_size='22sp',
            color=(1, 0.84, 0, 1),
            bold=True,
            font_name='DefaultFont'
        ))
        
        main_layout.add_widget(nav_bar)
        
        # 统计概览
        self.stats_box = BoxLayout(orientation='vertical', size_hint_y=0.25, spacing=8)
        self.update_stats(0)
        main_layout.add_widget(self.stats_box)
        
        # 成就列表
        scroll = ScrollView(size_hint_y=0.6)
        self.achievements_grid = GridLayout(cols=1, spacing=10, padding=10, size_hint_y=None)
        self.achievements_grid.bind(minimum_height=self.achievements_grid.setter('height'))
        
        self.create_achievements()
        
        scroll.add_widget(self.achievements_grid)
        main_layout.add_widget(scroll)
        
        self.add_widget(main_layout)
    
    def update_stats(self, dt):
        """更新统计"""
        self.stats_box.clear_widgets()
        
        achievements = game_data.get_achievements()
        pig = game_data.get_pig_status()
        
        # 标题
        self.stats_box.add_widget(Label(
            text='[统计] 学习统计',
            font_size='20sp',
            color=(0.3, 0.7, 0.9, 1),
            bold=True,
            size_hint_y=0.25,
            font_name='DefaultFont'
        ))
        
        # 统计数据行
        stats_row = BoxLayout(spacing=10, size_hint_y=0.35)
        
        stats_data = [
            ('[书] 答题总数', achievements.get('questions_answered', 0)),
            ('[对] 正确答题', achievements.get('correct_answers', 0)),
            ('[猪] 猪小弟等级', pig.get('level', 1))
        ]
        
        for label, value in stats_data:
            box = BoxLayout(orientation='vertical')
            box.add_widget(Label(text=label, font_size='14sp', color=(0.5, 0.5, 0.5, 1), font_name='DefaultFont'))
            box.add_widget(Label(text=str(value), font_size='24sp', bold=True, font_name='DefaultFont'))
            stats_row.add_widget(box)
        
        self.stats_box.add_widget(stats_row)
        
        # 正确率
        total = achievements.get('questions_answered', 0)
        correct = achievements.get('correct_answers', 0)
        rate = (correct / total * 100) if total > 0 else 0
        
        self.stats_box.add_widget(Label(
            text=f'[靶] 正确率: {rate:.1f}%',
            font_size='16sp',
            color=(0.4, 0.8, 0.4, 1) if rate >= 80 else (0.9, 0.7, 0.2, 1) if rate >= 60 else (0.9, 0.4, 0.4, 1),
            size_hint_y=0.25,
            font_name='DefaultFont'
        ))
    
    def create_achievements(self):
        """创建成就列表"""
        achievements = [
            {
                'icon': '[星]',
                'name': '初出茅庐',
                'desc': '完成第一次答题',
                'condition': lambda: game_data.get_achievements().get('questions_answered', 0) >= 1
            },
            {
                'icon': '[书]',
                'name': '小学者',
                'desc': '累计答对10道题',
                'condition': lambda: game_data.get_achievements().get('correct_answers', 0) >= 10
            },
            {
                'icon': '[帽]',
                'name': '小学霸',
                'desc': '累计答对50道题',
                'condition': lambda: game_data.get_achievements().get('correct_answers', 0) >= 50
            },
            {
                'icon': '[奖杯]',
                'name': '知识达人',
                'desc': '累计答对100道题',
                'condition': lambda: game_data.get_achievements().get('correct_answers', 0) >= 100
            },
            {
                'icon': '[猪]',
                'name': '小猪饲养员',
                'desc': '猪小弟达到3级',
                'condition': lambda: game_data.get_pig_status().get('level', 1) >= 3
            },
            {
                'icon': '[彩虹]',
                'name': '猪小弟大师',
                'desc': '猪小弟达到10级',
                'condition': lambda: game_data.get_pig_status().get('level', 1) >= 10
            },
            {
                'icon': '[金币]',
                'name': '小富翁',
                'desc': '拥有500金币',
                'condition': lambda: game_data.get_coins() >= 500
            },
            {
                'icon': '[皇冠]',
                'name': '大富翁',
                'desc': '拥有1000金币',
                'condition': lambda: game_data.get_coins() >= 1000
            },
            {
                'icon': '[靶]',
                'name': '答题高手',
                'desc': '正确率达到80%',
                'condition': lambda: self.get_accuracy() >= 80
            },
            {
                'icon': '[五星]',
                'name': '完美答题',
                'desc': '正确率达到100%（至少答20题）',
                'condition': lambda: self.get_accuracy() == 100 and game_data.get_achievements().get('questions_answered', 0) >= 20
            }
        ]
        
        for ach in achievements:
            unlocked = ach['condition']()
            self.create_achievement_card(ach, unlocked)
    
    def create_achievement_card(self, achievement, unlocked):
        """创建成就卡片"""
        card = BoxLayout(size_hint_y=None, height=80, padding=10)
        
        # 背景色根据解锁状态
        if unlocked:
            bg_color = (0.9, 0.95, 0.9, 1)
            status = '[对] 已解锁'
            status_color = (0.3, 0.8, 0.3, 1)
        else:
            bg_color = (0.95, 0.95, 0.95, 1)
            status = '[锁] 未解锁'
            status_color = (0.6, 0.6, 0.6, 1)
        
        # 图标
        icon_label = Label(
            text=achievement['icon'],
            font_size='24sp',
            size_hint_x=0.2,
            font_name='DefaultFont'
        )
        card.add_widget(icon_label)
        
        # 信息
        info_box = BoxLayout(orientation='vertical', size_hint_x=0.5)
        info_box.add_widget(Label(
            text=achievement['name'],
            font_size='18sp',
            bold=True,
            halign='left',
            color=(0.2, 0.2, 0.2, 1) if unlocked else (0.5, 0.5, 0.5, 1),
            font_name='DefaultFont'
        ))
        info_box.add_widget(Label(
            text=achievement['desc'],
            font_size='14sp',
            halign='left',
            color=(0.5, 0.5, 0.5, 1),
            font_name='DefaultFont'
        ))
        card.add_widget(info_box)
        
        # 状态
        status_label = Label(
            text=status,
            font_size='14sp',
            size_hint_x=0.3,
            color=status_color,
            font_name='DefaultFont'
        )
        card.add_widget(status_label)
        
        self.achievements_grid.add_widget(card)
    
    def get_accuracy(self):
        """获取正确率"""
        achievements = game_data.get_achievements()
        total = achievements.get('questions_answered', 0)
        correct = achievements.get('correct_answers', 0)
        return (correct / total * 100) if total > 0 else 0
    
    def go_back(self):
        """返回首页"""
        self.manager.current = 'home'
    
    def on_enter(self):
        """进入屏幕时刷新"""
        self.achievements_grid.clear_widgets()
        self.create_achievements()
        self.update_stats(0)
