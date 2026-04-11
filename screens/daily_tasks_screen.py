from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.popup import Popup
from kivy.uix.image import Image
from kivy.clock import Clock
from kivy.properties import NumericProperty
from datetime import datetime, timedelta
from data.game_data import game_data


class DailyTasksScreen(Screen):
    """每日任务屏幕"""
    
    completed_count = NumericProperty(0)
    total_count = NumericProperty(5)
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.tasks = []
        self.build_ui()
        Clock.schedule_interval(self.update_ui, 2)
    
    def build_ui(self):
        main_layout = BoxLayout(orientation='vertical', padding=15, spacing=10)
        
        # 顶部导航
        nav_bar = BoxLayout(size_hint_y=0.08, spacing=10)
        
        # 返回按钮（图标）
        back_box = BoxLayout(size_hint_x=0.15)
        back_icon = Image(source='assets/images/buttons/back.png', allow_stretch=True, keep_ratio=True)
        back_btn = Button(background_color=(0.6, 0.6, 0.6, 0.8), background_normal='')
        back_btn.bind(on_press=lambda x: self.go_back())
        back_box.add_widget(back_icon)
        back_box.add_widget(back_btn)
        nav_bar.add_widget(back_box)
        
        nav_bar.add_widget(Label(
            text='每日任务',
            font_size='22sp',
            color=(0.4, 0.8, 0.4, 1),
            bold=True,
            font_name='DefaultFont'
        ))
        
        main_layout.add_widget(nav_bar)
        
        # 进度概览
        self.progress_box = BoxLayout(orientation='vertical', size_hint_y=0.15, spacing=5)
        self.progress_box.add_widget(Label(
            text='今日任务进度',
            font_size='18sp',
            color=(0.3, 0.7, 0.9, 1),
            font_name='DefaultFont'
        ))
        self.progress_label = Label(
            text='0/5 完成',
            font_size='24sp',
            bold=True,
            color=(0.4, 0.8, 0.4, 1),
            font_name='DefaultFont'
        )
        self.progress_box.add_widget(self.progress_label)
        main_layout.add_widget(self.progress_box)
        
        # 任务列表
        self.tasks_grid = GridLayout(cols=1, spacing=10, padding=10, size_hint_y=0.7)
        self.tasks_grid.bind(minimum_height=self.tasks_grid.setter('height'))
        
        main_layout.add_widget(self.tasks_grid)
        
        # 全部领取按钮
        self.claim_all_btn = Button(
            text='领取全部奖励',
            font_size='18sp',
            size_hint_y=0.08,
            background_color=(1, 0.84, 0, 1),
            background_normal='',
            font_name='DefaultFont'
        )
        self.claim_all_btn.bind(on_press=self.claim_all_rewards)
        main_layout.add_widget(self.claim_all_btn)
        
        self.add_widget(main_layout)
        
        # 初始化任务
        self.init_daily_tasks()
    
    def init_daily_tasks(self):
        """初始化每日任务"""
        # 检查是否是新的一天
        last_date = game_data.data.get('daily_tasks', {}).get('last_date', '')
        today = datetime.now().strftime('%Y-%m-%d')
        
        if last_date != today:
            # 新的一天，重置任务
            game_data.data['daily_tasks'] = {
                'last_date': today,
                'tasks': self.generate_daily_tasks(),
                'claimed_rewards': []
            }
            game_data.save_data()
        
        self.load_tasks()
    
    def generate_daily_tasks(self):
        """生成每日任务"""
        pig = game_data.get_pig_status()
        
        tasks = [
            {
                'id': 'quiz_10',
                'title': '学习小达人',
                'desc': '完成10道题目',
                'target': 10,
                'current': game_data.data['daily_tasks'].get('questions_today', 0),
                'reward_coins': 50,
                'reward_item': None,
                'completed': False,
                'claimed': False
            },
            {
                'id': 'correct_5',
                'title': '答题能手',
                'desc': '答对5道题目',
                'target': 5,
                'current': 0,  # 需要记录今日正确数
                'reward_coins': 30,
                'reward_item': None,
                'completed': False,
                'claimed': False
            },
            {
                'id': 'feed_pig',
                'title': '细心饲养员',
                'desc': '喂养猪小弟3次',
                'target': 3,
                'current': 0,
                'reward_coins': 30,
                'reward_item': '普通饲料',
                'completed': False,
                'claimed': False
            },
            {
                'id': 'play_with_pig',
                'title': '快乐互动',
                'desc': '与猪小弟互动或玩耍3次',
                'target': 3,
                'current': 0,
                'reward_coins': 20,
                'reward_item': '玩具球',
                'completed': False,
                'claimed': False
            },
            {
                'id': 'login',
                'title': '每日签到',
                'desc': '今日登录游戏',
                'target': 1,
                'current': 1,
                'reward_coins': 20,
                'reward_item': None,
                'completed': True,
                'claimed': False
            }
        ]
        return tasks
    
    def load_tasks(self):
        """加载任务列表"""
        self.tasks = game_data.data.get('daily_tasks', {}).get('tasks', [])
        self.update_task_display()
    
    def update_task_display(self):
        """更新任务显示"""
        self.tasks_grid.clear_widgets()
        
        completed = 0
        for task in self.tasks:
            if task['completed']:
                completed += 1
            self.create_task_card(task)
        
        self.completed_count = completed
        self.progress_label.text = f'{completed}/{self.total_count} 完成'
    
    def create_task_card(self, task):
        """创建任务卡片"""
        card = BoxLayout(size_hint_y=None, height=90, padding=10, spacing=10)
        
        # 根据状态设置背景色
        if task['claimed']:
            bg_color = (0.85, 0.85, 0.85, 1)
            status_text = '已领取'
            btn_disabled = True
        elif task['completed']:
            bg_color = (0.9, 0.95, 0.9, 1)
            status_text = '可领取'
            btn_disabled = False
        else:
            bg_color = (0.95, 0.95, 0.95, 1)
            status_text = f'{task["current"]}/{task["target"]}'
            btn_disabled = True
        
        # 任务信息
        info_box = BoxLayout(orientation='vertical', size_hint_x=0.6)
        info_box.add_widget(Label(
            text=task['title'],
            font_size='16sp',
            bold=True,
            halign='left',
            color=(0.2, 0.2, 0.2, 1) if not task['claimed'] else (0.5, 0.5, 0.5, 1),
            font_name='DefaultFont'
        ))
        info_box.add_widget(Label(
            text=task['desc'],
            font_size='14sp',
            halign='left',
            color=(0.5, 0.5, 0.5, 1),
            font_name='DefaultFont'
        ))
        reward_text = f'[金币] {task["reward_coins"]}'
        if task['reward_item']:
            reward_text += f' + {task["reward_item"]}'
        info_box.add_widget(Label(
            text=reward_text,
            font_size='12sp',
            halign='left',
            color=(1, 0.84, 0, 1),
            font_name='DefaultFont'
        ))
        card.add_widget(info_box)
        
        # 状态/按钮
        if task['claimed']:
            status_label = Label(
                text=status_text,
                font_size='14sp',
                size_hint_x=0.25,
                color=(0.5, 0.5, 0.5, 1),
                font_name='DefaultFont'
            )
            card.add_widget(status_label)
        else:
            claim_btn = Button(
                text=status_text,
                font_size='14sp',
                size_hint_x=0.25,
                background_color=(0.4, 0.8, 0.4, 1) if task['completed'] else (0.7, 0.7, 0.7, 1),
                disabled=btn_disabled,
                font_name='DefaultFont'
            )
            claim_btn.bind(on_press=lambda x, t=task: self.claim_reward(t))
            card.add_widget(claim_btn)
        
        self.tasks_grid.add_widget(card)
    
    def claim_reward(self, task):
        """领取任务奖励"""
        if task['completed'] and not task['claimed']:
            # 发放奖励
            game_data.add_coins(task['reward_coins'])
            if task['reward_item']:
                from data.questions import FOODS, ITEMS
                if task['reward_item'] in FOODS:
                    game_data.add_food(task['reward_item'])
                elif task['reward_item'] in ITEMS:
                    game_data.add_item(task['reward_item'])
            
            # 标记为已领取
            task['claimed'] = True
            game_data.save_data()
            
            # 显示奖励
            reward_msg = f'[金币] +{task["reward_coins"]}'
            if task['reward_item']:
                reward_msg += f'\n{task["reward_item"]} x1'
            self.show_message(f'[庆祝] 任务完成！\n{reward_msg}')
            
            # 刷新显示
            self.update_task_display()
    
    def claim_all_rewards(self, instance):
        """领取所有可领取的奖励"""
        claimed_any = False
        total_coins = 0
        total_items = []
        
        for task in self.tasks:
            if task['completed'] and not task['claimed']:
                game_data.add_coins(task['reward_coins'])
                total_coins += task['reward_coins']
                
                if task['reward_item']:
                    from data.questions import FOODS, ITEMS
                    if task['reward_item'] in FOODS:
                        game_data.add_food(task['reward_item'])
                    elif task['reward_item'] in ITEMS:
                        game_data.add_item(task['reward_item'])
                    total_items.append(task['reward_item'])
                
                task['claimed'] = True
                claimed_any = True
        
        if claimed_any:
            game_data.save_data()
            reward_msg = f'[金币] +{total_coins}'
            if total_items:
                reward_msg += f'\n获得了: {", ".join(total_items)}'
            self.show_message(f'[庆祝] 全部领取成功！\n{reward_msg}')
            self.update_task_display()
        else:
            self.show_message('[提示] 没有可领取的奖励\n快去做任务吧！')
    
    def update_task_progress(self, task_id, progress=1):
        """更新任务进度"""
        for task in self.tasks:
            if task['id'] == task_id and not task['completed']:
                task['current'] += progress
                if task['current'] >= task['target']:
                    task['completed'] = True
                game_data.save_data()
                self.update_task_display()
                break
    
    def update_ui(self, dt):
        """定期更新UI"""
        self.update_task_display()
    
    def show_message(self, message):
        """显示消息"""
        popup = Popup(
            title='提示',
            content=Label(text=message, font_size='16sp', font_name='DefaultFont'),
            size_hint=(0.7, 0.3)
        )
        popup.open()
        Clock.schedule_once(lambda dt: popup.dismiss(), 1.5)
    
    def go_back(self):
        """返回首页"""
        self.manager.current = 'home'
    
    def on_enter(self):
        """进入屏幕时刷新"""
        self.init_daily_tasks()
        self.update_task_display()
