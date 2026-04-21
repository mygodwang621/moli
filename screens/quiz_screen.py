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
            size_hint=(1, 1),
            pos_hint={'x': 0, 'y': 0}
        )
        root_layout.add_widget(bg_image)

        # 主内容布局
        main_layout = BoxLayout(orientation='vertical', padding=15, spacing=8, size_hint=(1, 1))

        # ── 顶部导航 ──
        nav_bar = BoxLayout(size_hint_y=0.07, spacing=10)

        # 返回按钮（纯文字，无图标叠加）
        back_btn = Button(
            text='< 返回',
            font_size='16sp',
            size_hint_x=0.2,
            background_color=(0.5, 0.5, 0.6, 1),
            background_normal='',
            color=(1, 1, 1, 1),
            font_name='DefaultFont'
        )
        back_btn.bind(on_press=lambda x: self.go_back())
        nav_bar.add_widget(back_btn)

        self.subject_label = Label(
            text='选择科目',
            font_size='20sp',
            color=(0.3, 0.7, 0.9, 1),
            bold=True,
            font_name='DefaultFont',
            size_hint_x=0.55
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

        # ── 猪小弟形象展示区（上半，答题时显示） ──
        self.pig_area = BoxLayout(
            orientation='horizontal',
            size_hint_y=0.22,
            padding=[10, 5]
        )
        # 猪小弟图片
        self.quiz_pig_image = Image(
            source='assets/images/characters/pig_normal.png',
            allow_stretch=True,
            keep_ratio=True,
            size_hint_x=0.35
        )
        self.pig_area.add_widget(self.quiz_pig_image)

        # 对话气泡区
        bubble_box = BoxLayout(size_hint_x=0.65, padding=[5, 10])
        with bubble_box.canvas.before:
            Color(1, 1, 1, 0.88)
            bubble_box.bg_rect = Rectangle(pos=bubble_box.pos, size=bubble_box.size)
        bubble_box.bind(pos=lambda o, v: setattr(o.bg_rect, 'pos', v))
        bubble_box.bind(size=lambda o, v: setattr(o.bg_rect, 'size', v))
        self.pig_bubble_label = Label(
            text='加油！我陪你答题~',
            font_size='16sp',
            color=(0.3, 0.2, 0.5, 1),
            halign='center',
            valign='middle',
            font_name='DefaultFont'
        )
        self.pig_bubble_label.bind(size=lambda o, v: setattr(o, 'text_size', v))
        bubble_box.add_widget(self.pig_bubble_label)
        self.pig_area.add_widget(bubble_box)

        self.pig_area.opacity = 0  # 初始隐藏，答题时显示
        main_layout.add_widget(self.pig_area)

        # ── 科目选择区 ──
        self.subject_grid = GridLayout(cols=2, spacing=15, size_hint_y=0.35)

        subjects = [
            ('语文', '📖', (0.85, 0.35, 0.35, 1)),
            ('数学', '🔢', (0.25, 0.55, 0.88, 1)),
            ('英语', '🔤', (0.35, 0.72, 0.35, 1)),
            ('科学', '🔬', (0.7, 0.35, 0.85, 1))
        ]

        for subject, icon, color in subjects:
            btn = Button(
                text=f'{icon} {subject}',
                font_size='22sp',
                background_color=color,
                background_normal='',
                color=(1, 1, 1, 1),
                font_name='DefaultFont'
            )
            btn.bind(on_press=lambda x, s=subject: self.start_quiz(s))
            self.subject_grid.add_widget(btn)

        main_layout.add_widget(self.subject_grid)

        # ── 答题区（初始隐藏） ──
        self.quiz_area = BoxLayout(orientation='vertical', spacing=10, size_hint_y=0.57)
        self.quiz_area.opacity = 0
        self.quiz_area.disabled = True

        # 题目（带白色半透明背景，自动换行）
        question_box = BoxLayout(size_hint_y=0.3, padding=12)
        with question_box.canvas.before:
            Color(1, 1, 1, 0.92)
            question_box.rect = Rectangle(pos=question_box.pos, size=question_box.size)
        question_box.bind(pos=lambda obj, val: setattr(obj.rect, 'pos', val))
        question_box.bind(size=lambda obj, val: setattr(obj.rect, 'size', val))

        self.question_label = Label(
            text='',
            font_size='19sp',
            halign='center',
            valign='middle',
            text_size=(None, None),
            color=(0.15, 0.15, 0.15, 1),
            font_name='DefaultFont'
        )
        self.bind(size=self.update_question_text_size)

        question_box.add_widget(self.question_label)
        self.quiz_area.add_widget(question_box)

        # 选项按钮（深色背景 + 白色文字，确保可读）
        self.options_grid = GridLayout(cols=2, spacing=8, size_hint_y=0.55)
        option_colors = [
            (0.35, 0.55, 0.75, 1),   # 蓝
            (0.45, 0.65, 0.45, 1),   # 绿
            (0.75, 0.50, 0.30, 1),   # 橙
            (0.60, 0.40, 0.70, 1),   # 紫
        ]
        for i in range(4):
            btn = Button(
                text='',
                font_size='18sp',
                background_color=option_colors[i],
                background_normal='',
                color=(1, 1, 1, 1),   # 白色文字，确保可读
                font_name='DefaultFont'
            )
            btn.bind(on_press=lambda x, idx=i: self.check_answer(idx))
            self.option_buttons.append(btn)
            self.options_grid.add_widget(btn)

        self.quiz_area.add_widget(self.options_grid)

        # 下一题 / 确认按钮（文字+颜色，清晰可见）
        next_btn_box = BoxLayout(size_hint_y=0.15, padding=[60, 4])
        self.next_btn = Button(
            text='下一题 >',
            font_size='18sp',
            background_color=(0.25, 0.65, 0.88, 1),
            background_normal='',
            color=(1, 1, 1, 1),
            opacity=0,
            disabled=True,
            font_name='DefaultFont'
        )
        self.next_btn.bind(on_press=lambda x: self.next_question())
        next_btn_box.add_widget(self.next_btn)
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
        # 科目图标映射
        subject_icons = {'语文': '📖', '数学': '🔢', '英语': '🔤', '科学': '🔬'}
        icon = subject_icons.get(subject, '📚')
        self.subject_label.text = f'{icon} {subject}'

        # 获取该科目的题目
        self.questions = QUESTIONS.get(subject, []).copy()
        shuffle(self.questions)
        self.questions = self.questions[:5]  # 每次5题
        self.current_q_index = 0
        self.score = 0
        self.score_label.text = '得分: 0'

        # 切换界面：隐藏科目选择，显示答题区和猪小弟
        self.subject_grid.opacity = 0
        self.subject_grid.disabled = True
        self.pig_area.opacity = 1
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
            self.question_label.text = f'第 {self.current_q_index + 1}/{len(self.questions)} 题\n{q["question"]}'

            # 猪小弟鼓励话
            encourage_msgs = ['加油！我陪你答题~', '相信自己！', '你一定行的！', '仔细想想~', '这题不难的！']
            import random
            self.pig_bubble_label.text = random.choice(encourage_msgs)

            # 设置选项（重置颜色）
            option_colors = [
                (0.35, 0.55, 0.75, 1),
                (0.45, 0.65, 0.45, 1),
                (0.75, 0.50, 0.30, 1),
                (0.60, 0.40, 0.70, 1),
            ]
            for i, btn in enumerate(self.option_buttons):
                btn.text = q['options'][i]
                btn.background_color = option_colors[i]
                btn.color = (1, 1, 1, 1)
                btn.disabled = False

            self.next_btn.opacity = 0
            self.next_btn.disabled = True
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
        if self.current_q_index + 1 >= len(self.questions):
            self.next_btn.text = '查看结果 >'
        else:
            self.next_btn.text = '下一题 >'
    
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
        self.pig_area.opacity = 0
        self.quiz_area.opacity = 0
        self.quiz_area.disabled = True
        self.subject_label.text = '选择科目'
        self.score_label.text = '得分: 0'
        self.score = 0
    
    def go_back(self):
        """返回首页"""
        self.reset_quiz()
        self.manager.current = 'home'
