from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.popup import Popup
from kivy.uix.scrollview import ScrollView
from kivy.uix.image import Image
from kivy.clock import Clock
from kivy.properties import NumericProperty
from kivy.graphics import Color, Rectangle
from data.game_data import game_data
from data.questions import FOODS, ITEMS


def create_icon_button(icon_source, callback, bg_color=(0.6, 0.6, 0.6, 1)):
    """创建图标按钮"""
    box = BoxLayout()
    icon = Image(source=icon_source, allow_stretch=True, keep_ratio=True)
    btn = Button(background_color=bg_color, background_normal='', background_down='')
    btn.bind(on_press=callback)
    box.add_widget(icon)
    box.add_widget(btn)
    return box


class ShopScreen(Screen):
    """商店和背包屏幕"""
    
    coins = NumericProperty(100)
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.build_ui()
        Clock.schedule_interval(self.update_coins, 1)
    
    def build_ui(self):
        main_layout = BoxLayout(orientation='vertical', padding=15, spacing=10)
        
        # 顶部导航
        nav_bar = BoxLayout(size_hint_y=0.08, spacing=10)
        
        # 返回按钮（图标）
        back_btn = create_icon_button('assets/images/buttons/back.png', lambda x: self.go_back())
        back_btn.size_hint_x = 0.12
        nav_bar.add_widget(back_btn)
        
        # 标签页切换
        self.shop_tab = Button(
            text='商店',
            font_size='16sp',
            background_color=(0.4, 0.8, 0.4, 1),
            background_normal='',
            font_name='DefaultFont',
            size_hint_x=0.25
        )
        self.shop_tab.bind(on_press=lambda x: self.show_shop())
        nav_bar.add_widget(self.shop_tab)
        
        self.bag_tab = Button(
            text='背包',
            font_size='16sp',
            background_color=(0.7, 0.7, 0.7, 1),
            background_normal='',
            font_name='DefaultFont',
            size_hint_x=0.25
        )
        self.bag_tab.bind(on_press=lambda x: self.show_bag())
        nav_bar.add_widget(self.bag_tab)
        
        # 金币显示（带图标）
        coins_box = BoxLayout(size_hint_x=0.30, spacing=5)
        coin_icon = Image(source='assets/images/icons/coin.png', allow_stretch=True, keep_ratio=True, size_hint_x=0.3)
        self.coins_label = Label(
            text='100',
            font_size='18sp',
            color=(1, 0.84, 0, 1),
            bold=True,
            font_name='DefaultFont',
            size_hint_x=0.7
        )
        coins_box.add_widget(coin_icon)
        coins_box.add_widget(self.coins_label)
        nav_bar.add_widget(coins_box)
        
        main_layout.add_widget(nav_bar)
        
        # 内容区
        self.content_area = BoxLayout(orientation='vertical', size_hint_y=0.87)
        main_layout.add_widget(self.content_area)
        
        self.add_widget(main_layout)
        
        # 默认显示商店
        self.show_shop()
    
    def update_coins(self, dt):
        """更新金币显示"""
        self.coins = game_data.get_coins()
        self.coins_label.text = f'[金币] {self.coins}'
    
    def show_shop(self):
        """显示商店"""
        self.content_area.clear_widgets()
        self.shop_tab.background_color = (0.4, 0.8, 0.4, 1)
        self.bag_tab.background_color = (0.7, 0.7, 0.7, 1)
        
        # 创建滚动视图
        scroll = ScrollView()
        layout = GridLayout(cols=2, spacing=15, padding=15, size_hint_y=None)
        layout.bind(minimum_height=layout.setter('height'))
        
        # 食物区标题
        food_title = Label(
            text='[肉] 食物',
            font_size='20sp',
            size_hint_y=None,
            height=40,
            color=(0.95, 0.5, 0.3, 1),
            bold=True,
            font_name='DefaultFont'
        )
        layout.add_widget(food_title)
        layout.add_widget(Label(text=''))  # 占位
        
        # 食物商品
        food_icons = {
            '普通饲料': 'assets/images/foods/feed.png',
            '红苹果': 'assets/images/foods/apple.png',
            '美味蛋糕': 'assets/images/foods/cake.png',
            '超级大餐': 'assets/images/foods/meal.png',
            '爱心便当': 'assets/images/foods/bento.png',
        }
        for food_name, food_data in FOODS.items():
            icon_source = food_icons.get(food_name, '')
            btn = self.create_shop_item(
                food_name,
                food_data['price'],
                f'+{food_data["hunger"]}饱食 +{food_data["happiness"]}快乐',
                lambda x, fn=food_name, fd=food_data, price=food_data['price']: self.buy_item(fn, price, 'food', fd),
                icon_source
            )
            layout.add_widget(btn)
        
        # 道具区标题
        item_title = Label(
            text='[玩] 玩具道具',
            font_size='20sp',
            size_hint_y=None,
            height=40,
            color=(0.4, 0.7, 0.9, 1),
            bold=True,
            font_name='DefaultFont'
        )
        layout.add_widget(item_title)
        layout.add_widget(Label(text=''))  # 占位
        
        # 道具商品
        item_icons = {
            '玩具球': 'assets/images/items/ball.png',
            '泡泡机': 'assets/images/items/bubble.png',
            '故事书': 'assets/images/items/book.png',
        }
        for item_name, item_data in ITEMS.items():
            icon_source = item_icons.get(item_name, '')
            btn = self.create_shop_item(
                item_name,
                item_data['price'],
                f'+{item_data["happiness"]}快乐',
                lambda x, iname=item_name, idata=item_data, price=item_data['price']: self.buy_item(iname, price, 'item', idata),
                icon_source
            )
            layout.add_widget(btn)
        
        scroll.add_widget(layout)
        self.content_area.add_widget(scroll)
    
    def create_shop_item(self, name, price, effect, callback, icon_source=''):
        """创建商店商品按钮 - 带图片"""
        # 使用BoxLayout代替Button，更好地控制样式
        btn_container = BoxLayout(
            orientation='horizontal',
            size_hint_y=None,
            height=100,
            padding=10,
            spacing=10
        )
        
        # 设置背景色（使用canvas）
        with btn_container.canvas.before:
            Color(0.2, 0.4, 0.6, 1)  # 深蓝色背景
            btn_container.rect = Rectangle(pos=btn_container.pos, size=btn_container.size)
        
        def update_rect(instance, value):
            btn_container.rect.pos = instance.pos
            btn_container.rect.size = instance.size
        btn_container.bind(pos=update_rect, size=update_rect)
        
        # 左侧图片
        if icon_source:
            icon = Image(
                source=icon_source,
                size_hint_x=0.25,
                allow_stretch=True,
                keep_ratio=True
            )
            btn_container.add_widget(icon)
        
        # 右侧文字区域
        text_box = BoxLayout(orientation='vertical', size_hint_x=0.75)
        
        name_label = Label(
            text=name,
            font_size='16sp',
            bold=True,
            color=(1, 1, 1, 1),
            font_name='DefaultFont',
            size_hint_y=0.4
        )
        text_box.add_widget(name_label)
        
        price_label = Label(
            text=f'{price} 金币',
            font_size='14sp',
            color=(1, 0.84, 0, 1),
            font_name='DefaultFont',
            size_hint_y=0.3
        )
        text_box.add_widget(price_label)
        
        effect_label = Label(
            text=effect,
            font_size='11sp',
            color=(0.8, 0.9, 1, 1),
            font_name='DefaultFont',
            size_hint_y=0.3
        )
        text_box.add_widget(effect_label)
        
        btn_container.add_widget(text_box)
        
        # 添加点击事件
        btn = Button(
            background_color=(0, 0, 0, 0),
            size_hint=(1, 1),
            pos_hint={'center_x': 0.5, 'center_y': 0.5}
        )
        btn.bind(on_press=callback)
        btn_container.add_widget(btn)
        
        return btn_container
    
    def buy_item(self, name, price, item_type, item_data):
        """购买物品"""
        if game_data.spend_coins(price):
            if item_type == 'food':
                game_data.add_food(name)
            else:
                game_data.add_item(name)
            self.show_message(f'购买成功！\n{name} 已加入背包')
        else:
            self.show_message('金币不足！\n快去答题赚取金币吧')
    
    def show_bag(self):
        """显示背包 - 带图标装备栏"""
        self.content_area.clear_widgets()
        self.shop_tab.background_color = (0.7, 0.7, 0.7, 1)
        self.bag_tab.background_color = (0.4, 0.8, 0.4, 1)
        
        inventory = game_data.get_inventory()
        
        # 使用ScrollView支持滚动
        from kivy.uix.scrollview import ScrollView
        scroll = ScrollView()
        layout = BoxLayout(orientation='vertical', spacing=15, size_hint_y=None)
        layout.bind(minimum_height=layout.setter('height'))
        
        # ========== 食物区 ==========
        food_box = BoxLayout(orientation='vertical', size_hint_y=None, height=250)
        food_box.add_widget(Label(
            text='[肉] 我的食物',
            font_size='20sp',
            size_hint_y=None,
            height=40,
            color=(0.95, 0.5, 0.3, 1),
            bold=True,
            font_name='DefaultFont'
        ))
        
        foods = inventory.get('foods', {})
        has_food = False
        for qty in foods.values():
            if qty > 0:
                has_food = True
                break
        
        if has_food:
            food_grid = GridLayout(cols=4, spacing=10, padding=10, size_hint_y=None, height=180)
            # 食物图标映射
            food_icons = {
                '普通饲料': 'assets/images/foods/food_normal.png',
                '营养饲料': 'assets/images/foods/food_nutritious.png',
                '美味蛋糕': 'assets/images/foods/food_cake.png',
                '超级大餐': 'assets/images/foods/food_feast.png',
                '爱心便当': 'assets/images/foods/food_bento.png'
            }
            
            for food_name, quantity in foods.items():
                if quantity > 0:
                    # 创建装备栏项
                    item_box = self._create_inventory_item(
                        food_icons.get(food_name, 'assets/images/foods/food_normal.png'),
                        food_name,
                        quantity,
                        (0.95, 0.7, 0.4, 1)  # 橙色背景
                    )
                    food_grid.add_widget(item_box)
            food_box.add_widget(food_grid)
        else:
            food_box.add_widget(Label(
                text='背包是空的\n快去商店购买吧！',
                font_size='16sp',
                font_name='DefaultFont',
                color=(0.7, 0.7, 0.7, 1)
            ))
        
        layout.add_widget(food_box)
        
        # ========== 道具区 ==========
        item_box = BoxLayout(orientation='vertical', size_hint_y=None, height=250)
        item_box.add_widget(Label(
            text='[玩] 我的道具',
            font_size='20sp',
            size_hint_y=None,
            height=40,
            color=(0.4, 0.7, 0.9, 1),
            bold=True,
            font_name='DefaultFont'
        ))
        
        items = inventory.get('items', {})
        has_item = False
        for qty in items.values():
            if qty > 0:
                has_item = True
                break
        
        if has_item:
            item_grid = GridLayout(cols=4, spacing=10, padding=10, size_hint_y=None, height=180)
            # 道具图标映射
            item_icons = {
                '玩具球': 'assets/images/items/item_ball.png',
                '飞盘': 'assets/images/items/item_frisbee.png',
                '毛绒玩具': 'assets/images/items/item_plush.png',
                '泡泡机': 'assets/images/items/item_bubble.png',
                '音乐盒': 'assets/images/items/item_music.png'
            }
            
            for item_name, quantity in items.items():
                if quantity > 0:
                    # 创建装备栏项
                    item_widget = self._create_inventory_item(
                        item_icons.get(item_name, 'assets/images/items/item_ball.png'),
                        item_name,
                        quantity,
                        (0.4, 0.8, 0.9, 1)  # 蓝色背景
                    )
                    item_grid.add_widget(item_widget)
            item_box.add_widget(item_grid)
        else:
            item_box.add_widget(Label(
                text='还没有道具\n快去商店购买吧！',
                font_size='16sp',
                font_name='DefaultFont',
                color=(0.7, 0.7, 0.7, 1)
            ))
        
        layout.add_widget(item_box)
        
        scroll.add_widget(layout)
        self.content_area.add_widget(scroll)
    
    def _create_inventory_item(self, icon_path, name, quantity, bg_color):
        """创建背包物品项（图标+名称+数量）"""
        from kivy.uix.relativelayout import RelativeLayout
        
        # 主容器
        container = BoxLayout(orientation='vertical', spacing=5, padding=5)
        
        # 背景色
        with container.canvas.before:
            Color(*bg_color[:3], 0.3)
            container.bg_rect = Rectangle(pos=container.pos, size=container.size)
        container.bind(pos=lambda obj, val: setattr(container.bg_rect, 'pos', val))
        container.bind(size=lambda obj, val: setattr(container.bg_rect, 'size', val))
        
        # 图标
        icon = Image(
            source=icon_path,
            allow_stretch=True,
            keep_ratio=True,
            size_hint=(1, 0.6)
        )
        container.add_widget(icon)
        
        # 名称
        name_label = Label(
            text=name,
            font_size='12sp',
            font_name='DefaultFont',
            color=(1, 1, 1, 1),
            size_hint=(1, 0.2)
        )
        container.add_widget(name_label)
        
        # 数量（带背景）
        quantity_box = BoxLayout(size_hint=(1, 0.2))
        quantity_label = Label(
            text=f'×{quantity}',
            font_size='14sp',
            font_name='DefaultFont',
            color=(1, 0.84, 0, 1),
            bold=True
        )
        quantity_box.add_widget(quantity_label)
        container.add_widget(quantity_box)
        
        return container
    
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
        self.update_coins(0)
