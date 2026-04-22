from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.popup import Popup
from kivy.uix.progressbar import ProgressBar
from kivy.uix.image import Image
from kivy.uix.relativelayout import RelativeLayout
from kivy.clock import Clock
from kivy.properties import NumericProperty, ObjectProperty
from kivy.animation import Animation
from kivy.graphics import Color, Rectangle
import random
from data.game_data import game_data
from data.questions import FOODS, ITEMS


class PigHomeScreen(Screen):
    """猪小弟家园屏幕"""
    
    hunger = NumericProperty(80)
    happiness = NumericProperty(80)
    level = NumericProperty(1)
    growth = NumericProperty(0)
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.breathe_animation = None
        self.bubble_label = None
        self.build_ui()
        Clock.schedule_interval(self.update_ui, 1)
        # 启动呼吸动画
        Clock.schedule_once(self.start_breathe_animation, 1)
    
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
            text='猪小弟家园',
            font_size='22sp',
            color=(0.95, 0.5, 0.3, 1),
            bold=True,
            font_name='DefaultFont'
        ))
        
        main_layout.add_widget(nav_bar)
        
        # 猪小弟展示区（带装扮）
        pig_area = BoxLayout(orientation='vertical', size_hint_y=0.35, padding=10)
        
        # 猪小弟形象容器（使用Scatter实现缩放动画）
        from kivy.uix.scatter import Scatter
        self.pig_container = Scatter(
            size_hint=(0.8, 0.8),
            pos_hint={'center_x': 0.5, 'center_y': 0.5},
            do_rotation=False,
            do_translation=False,
            do_scale=False,
            scale=1.0
        )
        # 绑定点击事件
        self.pig_container.bind(on_touch_down=self.on_pig_touch)
        
        # 内部容器用于放置图片
        self.pig_inner = RelativeLayout(size=self.pig_container.size)
        self.pig_container.add_widget(self.pig_inner)
        
        # 基础猪形象（底层）
        self.pig_image = Image(
            source='assets/images/characters/pig_normal.png',
            allow_stretch=True,
            keep_ratio=True,
            size_hint=(1, 1),
            pos_hint={'center_x': 0.5, 'center_y': 0.5}
        )
        self.pig_inner.add_widget(self.pig_image)
        
        # 装扮图层（顶层）- 使用数据驱动的偏移量
        self.costume_images = {
            'hat': Image(allow_stretch=True, keep_ratio=True, opacity=0),
            'clothes': Image(allow_stretch=True, keep_ratio=True, opacity=0),
            'accessory': Image(allow_stretch=True, keep_ratio=True, opacity=0)
        }
        for img in self.costume_images.values():
            self.pig_inner.add_widget(img)
        
        pig_area.add_widget(self.pig_container)
        
        # 名字和等级
        self.pig_info = Label(
            text='猪小弟 | Lv.1',
            font_size='16sp',
            color=(0.95, 0.5, 0.3, 1),
            bold=True,
            font_name='DefaultFont',
            size_hint_y=0.15
        )
        pig_area.add_widget(self.pig_info)
        
        # 当前装扮显示
        self.outfit_label = Label(
            text='',
            font_size='11sp',
            color=(0.6, 0.4, 0.8, 1),
            font_name='DefaultFont',
            size_hint_y=0.1
        )
        pig_area.add_widget(self.outfit_label)
        
        main_layout.add_widget(pig_area)
        
        # 状态栏
        status_area = BoxLayout(orientation='vertical', size_hint_y=0.25, spacing=8)
        
        # 饱食度
        hunger_box = BoxLayout(spacing=10)
        hunger_box.add_widget(Label(text='饱食度:', size_hint_x=0.25, font_size='16sp', font_name='DefaultFont'))
        self.hunger_bar = ProgressBar(max=100, value=80, size_hint_x=0.5)
        hunger_box.add_widget(self.hunger_bar)
        self.hunger_label = Label(text='80/100', size_hint_x=0.25, font_size='14sp', font_name='DefaultFont')
        hunger_box.add_widget(self.hunger_label)
        status_area.add_widget(hunger_box)
        
        # 快乐值
        happy_box = BoxLayout(spacing=10)
        happy_box.add_widget(Label(text='快乐值:', size_hint_x=0.25, font_size='16sp', font_name='DefaultFont'))
        self.happy_bar = ProgressBar(max=100, value=80, size_hint_x=0.5)
        happy_box.add_widget(self.happy_bar)
        self.happy_label = Label(text='80/100', size_hint_x=0.25, font_size='14sp', font_name='DefaultFont')
        happy_box.add_widget(self.happy_label)
        status_area.add_widget(happy_box)
        
        # 成长值
        growth_box = BoxLayout(spacing=10)
        growth_box.add_widget(Label(text='成长值:', size_hint_x=0.25, font_size='16sp', font_name='DefaultFont'))
        self.growth_bar = ProgressBar(max=100, value=0, size_hint_x=0.5)
        growth_box.add_widget(self.growth_bar)
        self.growth_label = Label(text='0/100', size_hint_x=0.25, font_size='14sp', font_name='DefaultFont')
        growth_box.add_widget(self.growth_label)
        status_area.add_widget(growth_box)
        
        main_layout.add_widget(status_area)
        
        # 操作按钮区
        action_area = BoxLayout(size_hint_y=0.25, spacing=15)
        
        # 喂养按钮
        feed_btn = Button(
            text='喂养',
            font_size='20sp',
            background_color=(0.95, 0.6, 0.3, 1),
            background_normal='',
            font_name='DefaultFont'
        )
        feed_btn.bind(on_press=self.show_feed_menu)
        action_area.add_widget(feed_btn)
        
        # 玩耍按钮
        play_btn = Button(
            text='玩耍',
            font_size='20sp',
            background_color=(0.4, 0.7, 0.9, 1),
            background_normal='',
            font_name='DefaultFont'
        )
        play_btn.bind(on_press=self.show_play_menu)
        action_area.add_widget(play_btn)
        
        # 互动按钮
        interact_btn = Button(
            text='互动',
            font_size='20sp',
            background_color=(0.9, 0.5, 0.7, 1),
            background_normal='',
            font_name='DefaultFont'
        )
        interact_btn.bind(on_press=self.interact)
        action_area.add_widget(interact_btn)
        
        main_layout.add_widget(action_area)
        
        # 提示信息
        self.tip_label = Label(
            text='记得经常来看望猪小弟哦！',
            font_size='14sp',
            size_hint_y=0.07,
            color=(0.5, 0.5, 0.5, 1),
            font_name='DefaultFont'
        )
        main_layout.add_widget(self.tip_label)
        
        self.add_widget(main_layout)
    
    def update_ui(self, dt):
        """更新UI"""
        pig = game_data.get_pig_status()
        self.hunger = pig['hunger']
        self.happiness = pig['happiness']
        self.level = pig['level']
        self.growth = pig['growth']
        
        self.hunger_bar.value = self.hunger
        self.hunger_label.text = f'{self.hunger}/100'
        
        # 更新装扮显示
        self.update_costume_display()
        
        self.happy_bar.value = self.happiness
        self.happy_label.text = f'{self.happiness}/100'
        
        growth_needed = self.level * 100
        self.growth_bar.max = growth_needed
        self.growth_bar.value = self.growth
        self.growth_label.text = f'{self.growth}/{growth_needed}'
        
        self.pig_info.text = f'猪小弟 | Lv.{self.level}'
        
        # 根据状态改变图片
        if self.hunger < 30 or self.happiness < 30:
            self.pig_image.source = 'assets/images/characters/pig_hungry.png'
        elif self.happiness > 80:
            self.pig_image.source = 'assets/images/characters/pig_happy.png'
        else:
            self.pig_image.source = 'assets/images/characters/pig_normal.png'
    
    def update_costume_display(self, animate=True):
        """更新装扮显示 - 使用数据驱动的位置和淡入淡出过渡"""
        equipped = game_data.get_equipped_costumes()
        outfit_names = []
        
        # 导入装扮数据
        from screens.dressup_screen import COSTUMES
        
        for slot in ['hat', 'clothes', 'accessory']:
            costume_id = equipped.get(slot)
            img_widget = self.costume_images[slot]
            
            if costume_id and costume_id in COSTUMES.get(slot, {}):
                costume_data = COSTUMES[slot][costume_id]
                new_source = f'assets/images/costumes/{costume_data["file"]}'
                
                # 使用数据驱动的位置和尺寸
                pos_hint = costume_data.get('pos_hint', {'center_x': 0.5, 'center_y': 0.5})
                size_hint = costume_data.get('size_hint', {'x': 0.3, 'y': 0.3})
                
                # 应用尺寸和位置
                img_widget.size_hint = (size_hint['x'], size_hint['y'])
                img_widget.pos_hint = pos_hint
                
                # 检查是否需要切换图片
                if img_widget.source != new_source and animate:
                    # 淡入淡出过渡：旧图片淡出 -> 更换 -> 新图片淡入
                    self._animate_costume_change(img_widget, new_source)
                else:
                    img_widget.source = new_source
                    img_widget.opacity = 1
                
                outfit_names.append(costume_data['name'])
            else:
                # 无装扮，淡出
                if animate and img_widget.opacity > 0:
                    fade_out = Animation(opacity=0, duration=0.3)
                    fade_out.start(img_widget)
                else:
                    img_widget.opacity = 0
        
        # 更新装扮文字显示
        if outfit_names:
            self.outfit_label.text = '当前装扮: ' + ' | '.join(outfit_names)
        else:
            self.outfit_label.text = ''
    
    def _animate_costume_change(self, img_widget, new_source):
        """装扮切换动画：淡出 -> 更换 -> 淡入"""
        # 淡出
        fade_out = Animation(opacity=0, duration=0.15)
        
        def on_fade_out_complete(*args):
            # 更换图片
            img_widget.source = new_source
            # 淡入
            fade_in = Animation(opacity=1, duration=0.15)
            fade_in.start(img_widget)
        
        fade_out.bind(on_complete=on_fade_out_complete)
        fade_out.start(img_widget)
    
    def show_feed_menu(self, instance):
        """显示喂养菜单"""
        inventory = game_data.get_inventory()
        foods = inventory.get('foods', {})
        
        content = BoxLayout(orientation='vertical', padding=10, spacing=10)
        
        # 硬编码食物数据，避免编码问题
        FOODS_DATA = {
            "普通饲料": {"hunger": 20, "happiness": 5},
            "营养饲料": {"hunger": 50, "happiness": 10},
            "美味蛋糕": {"hunger": 30, "happiness": 30},
            "超级大餐": {"hunger": 100, "happiness": 50},
            "爱心便当": {"hunger": 60, "happiness": 40}
        }
        
        # 过滤掉数量为0的食物
        available_foods = []
        for food_name, quantity in foods.items():
            if quantity > 0:
                # 查找对应的食物数据
                food_data = FOODS_DATA.get(food_name)
                if food_data:
                    available_foods.append((food_name, quantity, food_data))
        
        if not available_foods:
            content.add_widget(Label(
                text='背包里没有食物了\n快去商店购买吧！',
                font_size='16sp',
                font_name='DefaultFont',
                color=(0.4, 0.4, 0.4, 1)
            ))
        else:
            content.add_widget(Label(
                text='选择要喂的食物：',
                font_size='18sp',
                size_hint_y=0.15,
                font_name='DefaultFont',
                color=(0.2, 0.2, 0.2, 1)
            ))
            
            grid = GridLayout(cols=2, spacing=10, size_hint_y=0.7)
            for food_name, quantity, food_data in available_foods:
                btn = Button(
                    text=f'{food_name}\n数量: {quantity}\n+{food_data["hunger"]}饱食 +{food_data["happiness"]}快乐',
                    font_size='14sp',
                    halign='center',
                    font_name='DefaultFont',
                    size_hint_y=None,
                    height=100,
                    background_color=(0.95, 0.9, 0.85, 1),  # 浅棕色背景
                    color=(0.2, 0.2, 0.2, 1)  # 深色文字
                )
                btn.bind(on_press=lambda x, fn=food_name, fd=food_data: self.feed(fn, fd))
                grid.add_widget(btn)
            
            content.add_widget(grid)
        
        close_btn = Button(
            text='关闭',
            size_hint_y=0.15,
            font_size='16sp',
            font_name='DefaultFont',
            background_color=(0.7, 0.7, 0.7, 1),
            color=(0.2, 0.2, 0.2, 1)
        )
        content.add_widget(close_btn)
        
        popup = Popup(
            title='喂养猪小弟',
            content=content,
            size_hint=(0.85, 0.7),
            background_color=(0.2, 0.2, 0.2, 1)
        )
        close_btn.bind(on_press=popup.dismiss)
        popup.open()
    
    def feed(self, food_name, food_data):
        """喂养"""
        success, level_reward = game_data.feed_pig(food_name, food_data)
        if success:
            # 更新图片为开心
            self.pig_image.source = 'assets/images/characters/pig_happy.png'
            
            msg = f'喂了{food_name}！\n饱食+{food_data["hunger"]} 快乐+{food_data["happiness"]}'
            if level_reward > 0:
                msg += f'\n猪小弟升级了！\n奖励 {level_reward} 金币'
            self.show_message(msg)
        else:
            self.show_message('喂养失败')
    
    def show_play_menu(self, instance):
        """显示玩耍菜单"""
        inventory = game_data.get_inventory()
        items = inventory.get('items', {})
        
        content = BoxLayout(orientation='vertical', padding=10, spacing=10)
        
        if not items:
            content.add_widget(Label(text='背包里没有玩具了\n快去商店购买吧！', font_size='16sp', font_name='DefaultFont'))
        else:
            content.add_widget(Label(text='选择玩具：', font_size='18sp', size_hint_y=0.15, font_name='DefaultFont'))
            
            grid = GridLayout(cols=2, spacing=10)
            for item_name, quantity in items.items():
                if quantity > 0:
                    item_data = ITEMS.get(item_name, {})
                    btn = Button(
                        text=f'{item_name}\n数量: {quantity}\n+{item_data.get("happiness", 0)}快乐',
                        font_size='14sp',
                        halign='center',
                        font_name='DefaultFont'
                    )
                    btn.bind(on_press=lambda x, iname=item_name, idata=item_data: self.play(iname, idata))
                    grid.add_widget(btn)
            
            content.add_widget(grid)
        
        close_btn = Button(text='关闭', size_hint_y=0.15, font_size='16sp', font_name='DefaultFont')
        content.add_widget(close_btn)
        
        popup = Popup(title='和猪小弟玩耍', content=content, size_hint=(0.85, 0.7))
        close_btn.bind(on_press=popup.dismiss)
        popup.open()
    
    def play(self, item_name, item_data):
        """玩耍"""
        success, level_reward = game_data.use_item(item_name, item_data)
        if success:
            # 更新图片为兴奋
            self.pig_image.source = 'assets/images/characters/pig_excited.png'
            
            msg = f'用了{item_name}和猪小弟玩耍！\n快乐+{item_data["happiness"]}'
            if level_reward > 0:
                msg += f'\n猪小弟升级了！\n奖励 {level_reward} 金币'
            self.show_message(msg)
        else:
            self.show_message('使用道具失败')
    
    def interact(self, instance):
        """互动"""
        pig = game_data.get_pig_status()
        
        if pig['happiness'] < 100:
            pig['happiness'] = min(100, pig['happiness'] + 5)
            pig['growth'] += 2  # 互动也增加成长值
            game_data.save_data()
            
            # 检查是否升级
            level_reward = game_data._check_level_up()
            if level_reward > 0:
                game_data.save_data()
                self.show_message(f'你摸了摸猪小弟的头\n快乐+5 成长+2\n猪小弟升级了！奖励 {level_reward} 金币')
            else:
                self.show_message('你摸了摸猪小弟的头\n快乐+5 成长+2')
        else:
            self.show_message('猪小弟已经很开心了！')
    
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
        """进入屏幕时更新"""
        self.update_ui(0)
    
    # ==================== 动画系统 ====================
    
    def start_breathe_animation(self, dt=None):
        """启动呼吸动画 - 每隔3秒轻微放大缩小"""
        # Kivy 使用 scale 属性（不是 scale_x/scale_y）
        # 创建呼吸动画：scale 1.0 -> 1.05 -> 1.0
        anim_up = Animation(scale=1.05, duration=0.5, t='in_out_quad')
        anim_down = Animation(scale=1.0, duration=0.5, t='in_out_quad')
        
        # 组合动画
        breathe = anim_up + anim_down
        breathe.bind(on_complete=lambda *args: Clock.schedule_once(self.start_breathe_animation, 2))
        
        # 应用到猪容器
        breathe.start(self.pig_container)
    
    def on_pig_touch(self, instance, touch):
        """点击猪小弟触发跳动动画和气泡"""
        if instance.collide_point(*touch.pos):
            self.play_jump_animation()
            self.show_bubble_text()
            return True
        return False
    
    def play_jump_animation(self):
        """跳动动画：向上位移20px，伴随挤压变形"""
        # 向上跳起 + 轻微挤压（scale=1.1）
        jump_up = Animation(
            pos_hint={'center_x': 0.5, 'center_y': 0.6},
            scale=1.1,
            duration=0.15,
            t='out_quad'
        )
        
        # 落下 + 落地挤压（scale=0.9）
        jump_down = Animation(
            pos_hint={'center_x': 0.5, 'center_y': 0.5},
            scale=0.9,
            duration=0.15,
            t='in_quad'
        )
        
        # 恢复原状（scale=1.0）
        recover = Animation(
            scale=1.0,
            duration=0.1,
            t='out_quad'
        )
        
        # 组合动画
        jump_anim = jump_up + jump_down + recover
        jump_anim.start(self.pig_container)
    
    def show_bubble_text(self):
        """显示随机气泡文字"""
        # 随机选择文字
        messages = ["哼唧~", "开心！", "好舒服~", "喜欢你~", "嘻嘻~", "抱抱~"]
        text = random.choice(messages)
        
        # 如果已有气泡，先移除
        if self.bubble_label and self.bubble_label.parent:
            self.bubble_label.parent.remove_widget(self.bubble_label)
        
        # 创建气泡标签
        self.bubble_label = Label(
            text=text,
            font_size='18sp',
            color=(0.95, 0.3, 0.5, 1),
            bold=True,
            font_name='DefaultFont',
            size_hint=(None, None),
            size=(100, 40),
            pos_hint={'center_x': 0.5, 'top': 0.95}
        )
        
        # 添加背景装饰
        with self.bubble_label.canvas.before:
            Color(1, 1, 1, 0.9)
            self.bubble_bg = Rectangle(pos=self.bubble_label.pos, size=self.bubble_label.size)
        
        # 绑定位置更新
        self.bubble_label.bind(pos=self._update_bubble_bg)
        
        self.pig_inner.add_widget(self.bubble_label)
        
        # 淡入动画
        self.bubble_label.opacity = 0
        anim_in = Animation(opacity=1, duration=0.2)
        anim_in.start(self.bubble_label)
        
        # 2秒后消失
        def remove_bubble(dt):
            if self.bubble_label and self.bubble_label.parent:
                anim_out = Animation(opacity=0, duration=0.3)
                anim_out.bind(on_complete=lambda *args: self.pig_inner.remove_widget(self.bubble_label) if self.bubble_label else None)
                anim_out.start(self.bubble_label)
        
        Clock.schedule_once(remove_bubble, 2)
    
    def _update_bubble_bg(self, instance, value):
        """更新气泡背景位置"""
        if hasattr(self, 'bubble_bg'):
            self.bubble_bg.pos = value
            self.bubble_bg.size = instance.size
