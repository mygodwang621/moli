from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.popup import Popup
from kivy.uix.image import Image
from kivy.uix.floatlayout import FloatLayout
from kivy.properties import StringProperty, NumericProperty
from kivy.clock import Clock
from kivy.graphics import Color, Rectangle
from random import choice, shuffle
from data.questions import QUESTIONS
from data.game_data import game_data


class QuizScreen(Screen):
    """知识问答屏幕"""
    
    current_question = StringProperty('')
    current_subject = StringProperty('')
    score = NumericProperty(0)
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.questions = []
        self.current_q_index = 0
        self.option_buttons = []
        self.build_ui()
    
    def build_ui(self):
        # 使用FloatLayout作为根布局，方便添加背景
        root_layout = FloatLayout()
        
        # 添加背景图
        bg_image = Image(
            source='assets/images/backgrounds/home_bg.png',
            allow_stretch=True,
            keep_ratio=False,
            opacity=0.3  # 半透明，不影响阅读
        )
        root_layout.add_widget(bg_image)
        
        # 主内容布局
        main_layout = BoxLayout(orientation='vertical', padding=15, spacing=10, size_hint=(1, 1))
        
        # 顶部导航
        nav_bar = BoxLayout(size_hint_y=0.08, spacing=10)
        
        # 返回按钮（使用图标）
        back_btn_box = BoxLayout(size_hint_x=0.15)
        back_icon = Image(source='assets/images/buttons/back.png', allow_stretch=True, keep_ratio=True)
        back_btn = Button(
            background_color=(0.6, 0.6, 0.6, 0.8),
            background_normal='',
            font_name='DefaultFont'
        )
        back_btn.bind(on_press=lambda x: self.go_back())
        back_btn_box.add_widget(back_icon)
        back_btn_box.add_widget(back_btn)
        nav_bar.add_widget(back_btn_box)
        
        self.subject_label = Label(
            text='选择科目',
            font_size='20sp',
            color=(0.3, 0.7, 0.9, 1),
            bold=True,
            font_name='DefaultFont',
            size_hint_x=0.6
        )
        nav_bar.add_widget(self.subject_label)
        
        self.score_label = Label(
            text='得分: 0',
            font_size='16sp',
            size_hint_x=0.25,
            color=(1, 0.84, 0, 1),
            font_name='DefaultFont'
        )
        nav_bar.add_widget(self.score_label)
        
        main_layout.add_widget(nav_bar)
        
        # 科目选择区
        self.subject_grid = GridLayout(cols=2, spacing=15, size_hint_y=0.3)
        
        subjects = [
            ('[文] 语文', (0.9, 0.4, 0.4, 1)),
            ('[数] 数学', (0.3, 0.6, 0.9, 1)),
            ('[英] 英语', (0.4, 0.8, 0.4, 1)),
            ('[科] 科学', (0.8, 0.4, 0.9, 1))
        ]
        
        for subject, color in subjects:
            btn = Button(
                text=subject,
                font_size='22sp',
                background_color=color,
                background_normal='',
                font_name='DefaultFont'
            )
            btn.bind(on_press=lambda x, s=subject[4:]: self.start_quiz(s))
            self.subject_grid.add_widget(btn)
        
        main_layout.add_widget(self.subject_grid)
        
        # 答题区（初始隐藏）
        self.quiz_area = BoxLayout(orientation='vertical', spacing=15, size_hint_y=0.6)
        self.quiz_area.opacity = 0
        self.quiz_area.disabled = True
        
        # 题目（带背景，自动换行）
        question_box = BoxLayout(size_hint_y=0.35, padding=10)
        # 白色半透明背景
        with question_box.canvas.before:
            Color(1, 1, 1, 0.85)
            question_box.rect = Rectangle(pos=question_box.pos, size=question_box.size)
        question_box.bind(pos=lambda obj, val: setattr(obj.rect, 'pos', val))
        question_box.bind(size=lambda obj, val: setattr(obj.rect, 'size', val))
        
        self.question_label = Label(
            text='',
            font_size='20sp',
            halign='center',
            valign='middle',
            text_size=(None, None),  # 会在update中设置宽度
            color=(0.2, 0.2, 0.2, 1),
            font_name='DefaultFont'
        )
        # 绑定窗口大小变化时更新text_size
        self.bind(size=self.update_question_text_size)
        
        question_box.add_widget(self.question_label)
        self.quiz_area.add_widget(question_box)
        
        # 选项按钮
        self.options_grid = GridLayout(cols=2, spacing=10, size_hint_y=0.5)
        for i in range(4):
            btn = Button(
                text='',
                font_size='18sp',
                background_color=(0.9, 0.95, 1, 1),  # 浅蓝色背景
                color=(0.2, 0.2, 0.2, 1),  # 深色文字
                font_name='DefaultFont'
            )
            btn.bind(on_press=lambda x, idx=i: self.check_answer(idx))
            self.option_buttons.append(btn)
            self.options_grid.add_widget(btn)
        
        self.quiz_area.add_widget(self.options_grid)
        
        # 下一题按钮（使用图标）
        next_btn_box = BoxLayout(size_hint_y=0.12, padding=[50, 5])
        next_icon = Image(
            source='assets/images/buttons/next.png',
            allow_stretch=True,
            keep_ratio=True,
            opacity=0  # 初始隐藏
        )
        self.next_btn = Button(
            background_color=(0.3, 0.7, 0.9, 1),
            opacity=0,
            disabled=True,
            font_name='DefaultFont'
        )
        self.next_btn.bind(on_press=lambda x: self.next_question())
        next_btn_box.add_widget(next_icon)
        next_btn_box.add_widget(self.next_btn)
        self.next_btn_icon = next_icon  # 保存引用
        self.quiz_area.add_widget(next_btn_box)
        
        main_layout.add_widget(self.quiz_area)
        
        root_layout.add_widget(main_layout)
        self.add_widget(root_layout)
    
    def update_question_text_size(self, *args):
        """更新题目文本宽度以实现自动换行"""
        if hasattr(self, 'question_label'):
            # 设置text_size为标签宽度的90%，允许换行
            self.question_label.text_size = (self.width * 0.85, None)
    
    def start_quiz(self, subject):
        """开始答题"""
        self.current_subject = subject
        self.subject_label.text = f'[书] {subject}'
        
        # 获取该科目的题目
        self.questions = QUESTIONS.get(subject, []).copy()
        shuffle(self.questions)
        self.questions = self.questions[:5]  # 每次5题
        self.current_q_index = 0
        self.score = 0
        
        # 切换界面
        self.subject_grid.opacity = 0
        self.subject_grid.disabled = True
        self.quiz_area.opacity = 1
        self.quiz_area.disabled = False
        
        # 更新题目文本大小
        self.update_question_text_size()
        
        self.show_question()
    
    def show_question(self):
        """显示当前题目"""
        if self.current_q_index < len(self.questions):
            q = self.questions[self.current_q_index]
            self.current_question = q['question']
            self.question_label.text = f'第 {self.current_q_index + 1}/{len(self.questions)} 题\n\n{q["question"]}'
            
            # 设置选项
            for i, btn in enumerate(self.option_buttons):
                btn.text = q['options'][i]
                btn.background_color = (0.9, 0.9, 0.9, 1)
                btn.disabled = False
            
            self.next_btn.opacity = 0
            self.next_btn.disabled = True
            if hasattr(self, 'next_btn_icon'):
                self.next_btn_icon.opacity = 0
        else:
            self.show_result()
    
    def check_answer(self, selected_idx):
        """检查答案"""
        q = self.questions[self.current_q_index]
        correct_idx = q['answer']
        base_reward = q['reward']
        
        # 禁用所有按钮
        for btn in self.option_buttons:
            btn.disabled = True
        
        if selected_idx == correct_idx:
            # 答对了
            self.option_buttons[selected_idx].background_color = (0.4, 0.9, 0.4, 1)
            
            # 计算奖励（基础 + 连对加成）
            if 'streak' not in game_data.data:
                game_data.data['streak'] = 0
            streak = game_data.data['streak']
            streak += 1
            game_data.data['streak'] = streak
            
            # 连对加成：每连对1题，额外10%奖励，最高50%
            streak_bonus = min(streak * 0.1, 0.5)
            total_reward = int(base_reward * (1 + streak_bonus))
            
            # 等级加成：猪小弟等级越高，奖励越多
            pig_level = game_data.get_pig_status().get('level', 1)
            level_bonus = (pig_level - 1) * 2  # 每级+2金币
            total_reward += level_bonus
            
            self.score += total_reward
            self.score_label.text = f'得分: {self.score}'
            game_data.add_coins(total_reward)
            game_data.record_answer(correct=True)
            
            # 显示奖励信息
            bonus_text = f"连对x{streak}! " if streak > 1 else ""
            if level_bonus > 0:
                bonus_text += f"等级+{level_bonus} "
            self.show_feedback(True, f'答对了！+{total_reward}金币\n{bonus_text}')
        else:
            # 答错了，重置连对
            game_data.data['streak'] = 0
            game_data.save_data()
            
            self.option_buttons[selected_idx].background_color = (0.9, 0.4, 0.4, 1)
            self.option_buttons[correct_idx].background_color = (0.4, 0.9, 0.4, 1)
            game_data.record_answer(correct=False)
            self.show_feedback(False, f'答错了，正确答案是：{q["options"][correct_idx]}')
        
        self.next_btn.opacity = 1
        self.next_btn.disabled = False
        if hasattr(self, 'next_btn_icon'):
            self.next_btn_icon.opacity = 1
    
    def show_feedback(self, correct, message):
        """显示反馈"""
        color = (0.4, 0.9, 0.4, 1) if correct else (0.9, 0.4, 0.4, 1)
        title_text = '回答正确' if correct else '回答错误'
        popup = Popup(
            title=title_text,
            content=Label(text=message, font_size='18sp', font_name='DefaultFont'),
            size_hint=(0.7, 0.3),
            background_color=color
        )
        popup.open()
        Clock.schedule_once(lambda dt: popup.dismiss(), 1.5)
    
    def next_question(self):
        """下一题"""
        self.current_q_index += 1
        self.show_question()
    
    def show_result(self):
        """显示答题结果"""
        content = BoxLayout(orientation='vertical', padding=10, spacing=10)
        content.add_widget(Label(
            text=f'[庆祝] 答题完成！\n\n总得分: {self.score} 金币',
            font_size='22sp',
            font_name='DefaultFont'
        ))
        
        btn_box = BoxLayout(size_hint_y=0.3)
        back_btn = Button(text='返回首页', font_size='16sp', font_name='DefaultFont')
        btn_box.add_widget(back_btn)
        content.add_widget(btn_box)
        
        popup = Popup(
            title='答题结果',
            content=content,
            size_hint=(0.8, 0.5),
            auto_dismiss=False
        )
        back_btn.bind(on_press=lambda x: [popup.dismiss(), self.reset_quiz()])
        popup.open()
    
    def reset_quiz(self):
        """重置答题界面"""
        self.subject_grid.opacity = 1
        self.subject_grid.disabled = False
        self.quiz_area.opacity = 0
        self.quiz_area.disabled = True
        self.subject_label.text = '选择科目'
        self.score_label.text = '得分: 0'
        self.score = 0
    
    def go_back(self):
        """返回首页"""
        self.reset_quiz()
        self.manager.current = 'home'
