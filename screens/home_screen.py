from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.image import Image
from kivy.graphics import Color, Rectangle, RoundedRectangle
from kivy.properties import StringProperty, NumericProperty
from kivy.clock import Clock
from kivy.core.text import Label as CoreLabel
from kivy.core.window import Window
from data.game_data import game_data
import os


class HomeScreen(Screen):
    """首页 - 显示茉莉酱和猪小弟，导航到各功能"""
    
    coins = NumericProperty(100)
    pig_level = NumericProperty(1)
    pig_hunger = NumericProperty(80)
    pig_happiness = NumericProperty(80)
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.build_ui()
        Clock.schedule_interval(self.update_status, 1)
    
    def build_ui(self):
        # 主布局
        main_layout = BoxLayout(orientation='vertical', padding=15, spacing=10)
        
        # 顶部状态栏
        status_bar = self.create_status_bar()
        main_layout.add_widget(status_bar)
        
        # 角色展示区（包含标题和角色）
        character_area = self.create_character_area()
        main_layout.add_widget(character_area)
        
        # 功能按钮区
        buttons_area = self.create_buttons_area()
        main_layout.add_widget(buttons_area)
        
        self.add_widget(main_layout)
    
    def create_status_bar(self):
        """创建顶部状态栏 - 带图标"""
        bar = BoxLayout(size_hint_y=0.08, spacing=10)
        
        # 金币显示（带图标）
        coins_box = BoxLayout(spacing=5)
        coins_icon = Image(
            source='assets/images/icons/coin.png',
            size_hint_x=None,
            width=24
        )
        self.coins_label = Label(
            text='100',
            font_size='18sp',
            color=(1, 0.84, 0, 1),
            bold=True,
            font_name='DefaultFont',
            size_hint_x=None,
            width=60
        )
        coins_box.add_widget(coins_icon)
        coins_box.add_widget(self.coins_label)
        bar.add_widget(coins_box)
        
        # 猪小弟状态
        self.status_label = Label(
            text='Lv.1 | 饱食:80 | 快乐:80',
            font_size='16sp',
            color=(0.3, 0.7, 0.9, 1),
            font_name='DefaultFont'
        )
        bar.add_widget(self.status_label)
        
        return bar
    
    def create_character_area(self):
        """创建角色展示区 - 简化版"""
        # 主容器
        main_box = BoxLayout(orientation='vertical', size_hint_y=0.35, spacing=5)
        
        # 标题
        main_box.add_widget(Label(
            text='茉莉酱的学习乐园',
            font_size='22sp',
            color=(0.9, 0.3, 0.5, 1),
            bold=True,
            font_name='DefaultFont',
            size_hint_y=0.2
        ))
        
        # 角色区域 - 使用GridLayout更稳定
        from kivy.uix.gridlayout import GridLayout
        grid = GridLayout(cols=2, size_hint_y=0.8, padding=10, spacing=20)
        
        # 茉莉酱（左侧）
        molijiang_box = BoxLayout(orientation='vertical', spacing=2)
        # 使用图片
        molijiang_img = Image(
            source='assets/images/characters/molijiang.png',
            size_hint_y=0.65,
            allow_stretch=True,
            keep_ratio=True
        )
        molijiang_box.add_widget(molijiang_img)
        molijiang_box.add_widget(Label(
            text='茉莉酱',
            font_size='15sp',
            color=(0.9, 0.4, 0.6, 1),
            bold=True,
            font_name='DefaultFont',
            size_hint_y=0.2
        ))
        molijiang_box.add_widget(Label(
            text='二年级小学生',
            font_size='11sp',
            color=(0.5, 0.4, 0.6, 1),
            font_name='DefaultFont',
            size_hint_y=0.15
        ))
        grid.add_widget(molijiang_box)
        
        # 猪小弟（右侧）
        pig_box = BoxLayout(orientation='vertical', spacing=2)
        # 使用图片
        self.pig_image = Image(
            source='assets/images/characters/pig_normal.png',
            size_hint_y=0.6,
            allow_stretch=True,
            keep_ratio=True
        )
        pig_box.add_widget(self.pig_image)
        pig_box.add_widget(Label(
            text='猪小弟',
            font_size='14sp',
            color=(0.95, 0.5, 0.3, 1),
            bold=True,
            font_name='DefaultFont',
            size_hint_y=0.25
        ))
        self.pig_level_label = Label(
            text=f'等级 {self.pig_level}',
            font_size='10sp',
            color=(0.5, 0.5, 0.5, 1),
            font_name='DefaultFont',
            size_hint_y=0.15
        )
        pig_box.add_widget(self.pig_level_label)
        grid.add_widget(pig_box)
        
        main_box.add_widget(grid)
        return main_box
    
    def create_buttons_area(self):
        """创建功能按钮区"""
        grid = GridLayout(cols=2, spacing=15, size_hint_y=0.4, padding=20)
        
        # 知识问答按钮
        btn_quiz = self.create_menu_button(
            '知识问答',
            '开始学习，赢取奖励！',
            (0.3, 0.7, 0.9, 1),
            'quiz',
            'assets/images/buttons/study.png'
        )
        grid.add_widget(btn_quiz)
        
        # 猪小弟家园按钮
        btn_home = self.create_menu_button(
            '猪小弟家园',
            '喂养和照顾猪小弟',
            (0.95, 0.5, 0.3, 1),
            'pig_home',
            'assets/images/buttons/home.png'
        )
        grid.add_widget(btn_home)
        
        # 背包商店按钮
        btn_shop = self.create_menu_button(
            '背包商店',
            '购买食物和道具',
            (0.5, 0.8, 0.4, 1),
            'shop',
            'assets/images/buttons/shop.png'
        )
        grid.add_widget(btn_shop)
        
        # 学习报告按钮
        btn_report = self.create_menu_button(
            '学习报告',
            '查看学习统计',
            (0.3, 0.7, 0.9, 1),
            'report',
            'assets/images/buttons/report.png'
        )
        grid.add_widget(btn_report)
        
        # 每日任务按钮
        btn_daily = self.create_menu_button(
            '每日任务',
            '完成任务领奖励',
            (0.9, 0.5, 0.9, 1),
            'daily_tasks',
            'assets/images/buttons/tasks.png'
        )
        grid.add_widget(btn_daily)
        
        # 装扮商店按钮
        btn_dressup = self.create_menu_button(
            '装扮商店',
            '给猪小弟买新衣',
            (0.9, 0.6, 0.7, 1),
            'dressup',
            'assets/images/buttons/dressup.png'
        )
        grid.add_widget(btn_dressup)
        
        # 设置按钮
        btn_settings = self.create_menu_button(
            '游戏设置',
            '音效和关于',
            (0.5, 0.5, 0.5, 1),
            'settings',
            'assets/images/buttons/settings.png'
        )
        grid.add_widget(btn_settings)
        
        return grid
    
    def create_menu_button(self, title, desc, color, screen_name, icon_source=None):
        """创建菜单按钮 - 带图标，居中对齐"""
        from kivy.uix.anchorlayout import AnchorLayout
        
        # 主按钮布局 - 使用AnchorLayout确保内容居中
        btn_layout = BoxLayout(orientation='horizontal', padding=10, spacing=10)
        
        # 背景色
        with btn_layout.canvas.before:
            Color(*color)
            btn_layout.rect = RoundedRectangle(pos=btn_layout.pos, size=btn_layout.size, radius=[10])
        btn_layout.bind(pos=lambda obj, val: setattr(btn_layout.rect, 'pos', val))
        btn_layout.bind(size=lambda obj, val: setattr(btn_layout.rect, 'size', val))
        
        # 图标容器（垂直居中，小尺寸）
        if icon_source:
            icon_anchor = AnchorLayout(anchor_x='center', anchor_y='center', size_hint_x=0.25)
            icon = Image(
                source=icon_source,
                size_hint=(None, None),
                size=(32, 32),
                allow_stretch=True,
                keep_ratio=True
            )
            icon_anchor.add_widget(icon)
            btn_layout.add_widget(icon_anchor)
        
        # 文字区域（垂直居中）
        text_anchor = AnchorLayout(anchor_x='left', anchor_y='center', size_hint_x=0.75)
        text_box = BoxLayout(orientation='vertical', spacing=2)
        text_box.add_widget(Label(
            text=title,
            font_size='16sp',
            bold=True,
            color=(1, 1, 1, 1),
            font_name='DefaultFont',
            halign='left',
            size_hint_y=0.55
        ))
        text_box.add_widget(Label(
            text=desc,
            font_size='11sp',
            color=(0.95, 0.95, 0.95, 1),
            font_name='DefaultFont',
            halign='left',
            size_hint_y=0.45
        ))
        text_anchor.add_widget(text_box)
        btn_layout.add_widget(text_anchor)
        
        # 将整个布局放入一个可点击的按钮中
        btn = Button(
            background_color=(0, 0, 0, 0),
            background_normal='',
            background_down='',
            font_name='DefaultFont'
        )
        
        # 绑定点击事件
        btn.bind(on_press=lambda x: self.go_to_screen(screen_name))
        
        # 创建一个容器，将布局和按钮叠加
        from kivy.uix.relativelayout import RelativeLayout
        container = RelativeLayout()
        container.add_widget(btn_layout)
        container.add_widget(btn)
        
        return container
    
    def go_to_screen(self, screen_name):
        """跳转到指定屏幕"""
        self.manager.current = screen_name
    
    def update_status(self, dt):
        """更新状态显示"""
        pig = game_data.get_pig_status()
        self.coins = game_data.get_coins()
        self.pig_level = pig['level']
        self.pig_hunger = pig['hunger']
        self.pig_happiness = pig['happiness']
        
        self.coins_label.text = f'{self.coins}'
        self.status_label.text = f'Lv.{self.pig_level} | 饱食:{self.pig_hunger} | 快乐:{self.pig_happiness}'
        
        # 更新猪小弟图片
        if hasattr(self, 'pig_image'):
            if self.pig_hunger < 30 or self.pig_happiness < 30:
                self.pig_image.source = 'assets/images/characters/pig_hungry.png'
            elif self.pig_happiness > 80:
                self.pig_image.source = 'assets/images/characters/pig_happy.png'
            else:
                self.pig_image.source = 'assets/images/characters/pig_normal.png'
        
        # 更新等级标签
        if hasattr(self, 'pig_level_label'):
            self.pig_level_label.text = f'等级 {self.pig_level}'
    
    def on_enter(self):
        """进入屏幕时更新数据"""
        self.update_status(0)
