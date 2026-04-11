from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.switch import Switch
from kivy.uix.image import Image
from kivy.graphics import Color, Rectangle
from utils.sound_manager import sound_manager


class SettingsScreen(Screen):
    """设置屏幕"""
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.build_ui()
    
    def build_ui(self):
        main_layout = BoxLayout(orientation='vertical', padding=20, spacing=15)
        
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
            text='游戏设置',
            font_size='22sp',
            color=(0.5, 0.5, 0.5, 1),
            bold=True,
            font_name='DefaultFont'
        ))
        
        main_layout.add_widget(nav_bar)
        
        # 设置选项区域
        settings_box = BoxLayout(orientation='vertical', spacing=20, padding=20)
        
        # 音效开关
        sound_row = self.create_setting_row(
            '音效',
            '开启/关闭游戏音效',
            sound_manager.enabled,
            self.toggle_sound
        )
        settings_box.add_widget(sound_row)
        
        # 背景音乐开关
        bgm_row = self.create_setting_row(
            '背景音乐',
            '开启/关闭背景音乐',
            sound_manager.bgm_enabled,
            self.toggle_bgm
        )
        settings_box.add_widget(bgm_row)
        
        # 关于信息
        about_box = BoxLayout(orientation='vertical', size_hint_y=0.4, spacing=10)
        
        with about_box.canvas.before:
            Color(0.95, 0.95, 0.95, 1)
            about_box.rect = Rectangle(pos=about_box.pos, size=about_box.size)
        about_box.bind(pos=lambda obj, val: setattr(about_box.rect, 'pos', val))
        about_box.bind(size=lambda obj, val: setattr(about_box.rect, 'size', val))
        
        about_box.add_widget(Label(
            text='关于游戏',
            font_size='18sp',
            bold=True,
            color=(0.3, 0.3, 0.3, 1),
            font_name='DefaultFont'
        ))
        
        about_box.add_widget(Label(
            text='茉莉酱的学习乐园 v1.0',
            font_size='14sp',
            color=(0.5, 0.5, 0.5, 1),
            font_name='DefaultFont'
        ))
        
        about_box.add_widget(Label(
            text='专为深圳小学二年级学生设计',
            font_size='12sp',
            color=(0.6, 0.6, 0.6, 1),
            font_name='DefaultFont'
        ))
        
        about_box.add_widget(Label(
            text='题库: 语文/数学/英语/科学',
            font_size='12sp',
            color=(0.6, 0.6, 0.6, 1),
            font_name='DefaultFont'
        ))
        
        settings_box.add_widget(about_box)
        
        main_layout.add_widget(settings_box)
        self.add_widget(main_layout)
    
    def create_setting_row(self, title, desc, default_value, callback):
        """创建设置行"""
        row = BoxLayout(size_hint_y=None, height=80, padding=10, spacing=10)
        
        with row.canvas.before:
            Color(0.98, 0.98, 0.98, 1)
            row.rect = Rectangle(pos=row.pos, size=row.size)
        row.bind(pos=lambda obj, val: setattr(row.rect, 'pos', val))
        row.bind(size=lambda obj, val: setattr(row.rect, 'size', val))
        
        # 文字说明
        text_box = BoxLayout(orientation='vertical', size_hint_x=0.7)
        text_box.add_widget(Label(
            text=title,
            font_size='18sp',
            bold=True,
            halign='left',
            color=(0.2, 0.2, 0.2, 1),
            font_name='DefaultFont'
        ))
        text_box.add_widget(Label(
            text=desc,
            font_size='12sp',
            halign='left',
            color=(0.5, 0.5, 0.5, 1),
            font_name='DefaultFont'
        ))
        row.add_widget(text_box)
        
        # 开关
        switch = Switch(active=default_value, size_hint_x=0.3)
        switch.bind(active=callback)
        row.add_widget(switch)
        
        return row
    
    def toggle_sound(self, instance, value):
        """切换音效"""
        sound_manager.enabled = value
        status = '开启' if value else '关闭'
        print(f"[设置] 音效已{status}")
    
    def toggle_bgm(self, instance, value):
        """切换背景音乐"""
        sound_manager.bgm_enabled = value
        if value:
            print("[设置] 背景音乐已开启")
        else:
            print("[设置] 背景音乐已关闭")
    
    def go_back(self):
        """返回首页"""
        self.manager.current = 'home'
