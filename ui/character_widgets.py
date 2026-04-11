from kivy.uix.widget import Widget
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.graphics import Color, Ellipse, Rectangle, Line, Triangle
from kivy.properties import NumericProperty, StringProperty, ListProperty
from kivy.clock import Clock
from kivy.animation import Animation


class MolijiangWidget(BoxLayout):
    """茉莉酱角色组件"""
    
    def __init__(self, **kwargs):
        super().__init__(orientation='vertical', size_hint=(1, 1), **kwargs)
        
        # 添加文字标签（使用更大的字体）
        self.add_widget(Label(
            text='[茉莉酱]',
            font_size='100sp',
            font_name='DefaultFont',
            color=(0.9, 0.4, 0.6, 1),
            size_hint=(1, 0.8)
        ))


class PigWidget(BoxLayout):
    """猪小弟角色组件"""
    
    mood = StringProperty('normal')  # normal, happy, sad, excited
    
    def __init__(self, **kwargs):
        super().__init__(orientation='vertical', size_hint=(1, 1), **kwargs)
        
        # 表情符号映射
        self.mood_emojis = {
            'normal': '[猪]',
            'happy': '[猪-开心]',
            'sad': '[猪-困]',
            'excited': '[猪-兴奋]'
        }
        
        # 添加表情标签
        self.emoji_label = Label(
            text=self.mood_emojis['normal'],
            font_size='100sp',
            font_name='DefaultFont',
            color=(0.95, 0.5, 0.3, 1),
            size_hint=(1, 0.8)
        )
        self.add_widget(self.emoji_label)
    
    def set_mood(self, mood):
        """设置表情"""
        if mood in self.mood_emojis:
            self.mood = mood
            self.emoji_label.text = self.mood_emojis[mood]
            
            # 根据心情改变颜色
            if mood == 'happy':
                self.emoji_label.color = (0.4, 0.9, 0.4, 1)  # 绿色
            elif mood == 'sad':
                self.emoji_label.color = (0.6, 0.6, 0.6, 1)  # 灰色
            elif mood == 'excited':
                self.emoji_label.color = (0.9, 0.4, 0.9, 1)  # 紫色
            else:
                self.emoji_label.color = (0.95, 0.5, 0.3, 1)  # 橙色
    
    def eat_animation(self):
        """吃东西动画"""
        self.set_mood('happy')
        Clock.schedule_once(lambda dt: self.set_mood('normal'), 2)
    
    def play_animation(self):
        """玩耍动画"""
        self.set_mood('excited')
        Clock.schedule_once(lambda dt: self.set_mood('normal'), 2)


class AnimatedCoin(BoxLayout):
    """动画金币组件"""
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.size_hint = (None, None)
        self.size = (40, 40)
        
        self.add_widget(Label(
            text='[金币]',
            font_size='30sp',
            font_name='DefaultFont',
            color=(1, 0.84, 0, 1)
        ))
        
        # 旋转动画
        self.start_spin_animation()
    
    def start_spin_animation(self):
        """开始旋转动画"""
        anim = Animation(rotation=360, duration=2)
        anim.repeat = True
        anim.start(self)


class FloatingText(Label):
    """浮动文字效果（用于显示+金币等）"""
    
    def __init__(self, text, **kwargs):
        super().__init__(
            text=text,
            font_size='20sp',
            bold=True,
            font_name='DefaultFont',
            color=(1, 0.84, 0, 1),
            **kwargs
        )
        self.size_hint = (None, None)
        self.size = (100, 40)
    
    def animate(self, start_pos):
        """播放浮动动画"""
        self.pos = start_pos
        anim = Animation(y=start_pos[1] + 50, opacity=0, duration=1)
        anim.bind(on_complete=lambda *args: self.parent.remove_widget(self))
        anim.start(self)
