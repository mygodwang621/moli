from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.popup import Popup
from kivy.uix.scrollview import ScrollView
from kivy.uix.image import Image
from kivy.graphics import Color, Rectangle
from kivy.clock import Clock
from data.game_data import game_data


# 装扮数据 - 带偏移量配置
# pos_hint: 相对于猪小弟容器的位置 (0-1)，使用 top/y/center_x 等
# size_hint: 装扮图片的缩放比例
COSTUMES = {
    "hat": {
        "hat_bowler": {
            "name": "小礼帽", "price": 100, "bonus": "+5快乐", 
            "file": "hat_bowler.png",
            "pos_hint": {"center_x": 0.5, "top": 0.35},  # 顶部
            "size_hint": {"x": 0.5, "y": 0.4}
        },
        "hat_sun": {
            "name": "太阳帽", "price": 150, "bonus": "+8快乐", 
            "file": "hat_sun.png",
            "pos_hint": {"center_x": 0.5, "top": 0.38},
            "size_hint": {"x": 0.55, "y": 0.42}
        },
        "hat_crown": {
            "name": "皇冠", "price": 500, "bonus": "+15快乐", 
            "file": "hat_crown.png",
            "pos_hint": {"center_x": 0.5, "top": 0.32},
            "size_hint": {"x": 0.45, "y": 0.38}
        },
        "hat_student": {
            "name": "学生帽", "price": 80, "bonus": "+3快乐", 
            "file": "hat_student.png",
            "pos_hint": {"center_x": 0.5, "top": 0.36},
            "size_hint": {"x": 0.48, "y": 0.35}
        },
    },
    "clothes": {
        "clothes_vest": {
            "name": "小背心", "price": 120, "bonus": "+5饱食", 
            "file": "clothes_vest.png",
            "pos_hint": {"center_x": 0.5, "center_y": 0.45},  # 身体中间
            "size_hint": {"x": 0.6, "y": 0.55}
        },
        "clothes_sport": {
            "name": "运动服", "price": 200, "bonus": "+8饱食", 
            "file": "clothes_sport.png",
            "pos_hint": {"center_x": 0.5, "center_y": 0.42},
            "size_hint": {"x": 0.65, "y": 0.6}
        },
        "clothes_formal": {
            "name": "礼服", "price": 400, "bonus": "+12饱食", 
            "file": "clothes_formal.png",
            "pos_hint": {"center_x": 0.5, "center_y": 0.4},
            "size_hint": {"x": 0.68, "y": 0.65}
        },
        "clothes_uniform": {
            "name": "校服", "price": 100, "bonus": "+3饱食", 
            "file": "clothes_uniform.png",
            "pos_hint": {"center_x": 0.5, "center_y": 0.43},
            "size_hint": {"x": 0.62, "y": 0.58}
        },
    },
    "accessory": {
        "acc_bowtie": {
            "name": "领结", "price": 80, "bonus": "+3快乐", 
            "file": "acc_bowtie.png",
            "pos_hint": {"center_x": 0.5, "center_y": 0.55},  # 脖子位置
            "size_hint": {"x": 0.3, "y": 0.25}
        },
        "acc_glasses": {
            "name": "眼镜", "price": 150, "bonus": "+5快乐", 
            "file": "acc_glasses.png",
            "pos_hint": {"center_x": 0.5, "center_y": 0.62},  # 眼睛位置
            "size_hint": {"x": 0.5, "y": 0.3}
        },
        "acc_bell": {
            "name": "铃铛", "price": 200, "bonus": "+8快乐", 
            "file": "acc_bell.png",
            "pos_hint": {"center_x": 0.65, "center_y": 0.5},
            "size_hint": {"x": 0.25, "y": 0.3}
        },
        "acc_scarf": {
            "name": "围巾", "price": 120, "bonus": "+4快乐", 
            "file": "acc_scarf.png",
            "pos_hint": {"center_x": 0.5, "center_y": 0.52},
            "size_hint": {"x": 0.45, "y": 0.35}
        },
    }
}

CATEGORY_NAMES = {
    "hat": "帽子",
    "clothes": "衣服", 
    "accessory": "配饰"
}


class DressUpScreen(Screen):
    """装扮商店屏幕"""
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.current_category = "hat"
        self.build_ui()
        Clock.schedule_interval(self.update_ui, 1)
    
    def build_ui(self):
        main_layout = BoxLayout(orientation='vertical', padding=10, spacing=8)
        
        # 顶部导航
        nav_bar = BoxLayout(size_hint_y=0.07, spacing=8)
        
        # 返回按钮
        back_box = BoxLayout(size_hint_x=0.12)
        back_icon = Image(source='assets/images/buttons/back.png', allow_stretch=True, keep_ratio=True)
        back_btn = Button(background_color=(0.6, 0.6, 0.6, 0.8), background_normal='')
        back_btn.bind(on_press=lambda x: self.go_back())
        back_box.add_widget(back_icon)
        back_box.add_widget(back_btn)
        nav_bar.add_widget(back_box)
        
        nav_bar.add_widget(Label(
            text='装扮商店',
            font_size='20sp',
            color=(0.9, 0.5, 0.7, 1),
            bold=True,
            font_name='DefaultFont'
        ))
        
        # 金币显示
        coins_box = BoxLayout(size_hint_x=0.22, spacing=3)
        coin_icon = Image(source='assets/images/icons/coin.png', allow_stretch=True, keep_ratio=True)
        self.coins_label = Label(
            text='100',
            font_size='16sp',
            color=(1, 0.84, 0, 1),
            bold=True,
            font_name='DefaultFont'
        )
        coins_box.add_widget(coin_icon)
        coins_box.add_widget(self.coins_label)
        nav_bar.add_widget(coins_box)
        
        main_layout.add_widget(nav_bar)
        
        # 当前装扮展示区
        outfit_box = BoxLayout(orientation='vertical', size_hint_y=0.18, padding=5, spacing=3)
        with outfit_box.canvas.before:
            Color(0.98, 0.95, 0.9, 1)
            outfit_box.rect = Rectangle(pos=outfit_box.pos, size=outfit_box.size)
        outfit_box.bind(pos=lambda obj, val: setattr(obj.rect, 'pos', val))
        outfit_box.bind(size=lambda obj, val: setattr(obj.rect, 'size', val))
        
        outfit_box.add_widget(Label(
            text='当前装扮',
            font_size='14sp',
            color=(0.7, 0.4, 0.3, 1),
            bold=True,
            font_name='DefaultFont',
            size_hint_y=0.3
        ))
        
        self.outfit_display = BoxLayout(size_hint_y=0.7, spacing=10)
        outfit_box.add_widget(self.outfit_display)
        main_layout.add_widget(outfit_box)
        
        # 分类标签（带按下效果）
        category_bar = BoxLayout(size_hint_y=0.06, spacing=8)
        self.category_buttons = {}
        for cat_key, cat_name in CATEGORY_NAMES.items():
            # 使用自定义按钮容器实现按下效果
            btn_container = BoxLayout()
            btn = Button(
                text=cat_name,
                font_size='14sp',
                background_color=(0.75, 0.75, 0.75, 1),
                background_normal='',
                background_down='',  # 禁用默认按下效果
                font_name='DefaultFont'
            )
            # 绑定按下和释放事件
            btn.bind(on_press=lambda x, c=cat_key, b=btn: self.on_category_press(c, b))
            btn.bind(on_release=lambda x, b=btn: self.on_category_release(b))
            self.category_buttons[cat_key] = btn
            btn_container.add_widget(btn)
            category_bar.add_widget(btn_container)
        
        main_layout.add_widget(category_bar)
        
        # 装扮列表区
        self.items_area = BoxLayout(orientation='vertical', size_hint_y=0.69)
        main_layout.add_widget(self.items_area)
        
        self.add_widget(main_layout)
        self.show_category("hat")
    
    def on_category_press(self, category, btn):
        """分类按钮按下效果 - 向下位移2px并变暗"""
        # 变暗效果（降低亮度）
        original_color = btn.background_color
        btn._original_color = original_color
        btn.background_color = (original_color[0] * 0.7, original_color[1] * 0.7, 
                               original_color[2] * 0.7, original_color[3])
        # 显示分类
        self.show_category(category)
    
    def on_category_release(self, btn):
        """分类按钮释放效果 - 恢复原状"""
        if hasattr(btn, '_original_color'):
            btn.background_color = btn._original_color
    
    def update_ui(self, dt):
        """更新UI"""
        self.coins_label.text = str(game_data.get_coins())
        self.update_outfit_display()
    
    def update_outfit_display(self):
        """更新当前装扮显示"""
        self.outfit_display.clear_widgets()
        equipped = game_data.get_equipped_costumes()
        
        for slot in ['hat', 'clothes', 'accessory']:
            slot_box = BoxLayout(orientation='vertical', size_hint_x=0.33)
            costume_id = equipped.get(slot)
            
            if costume_id and costume_id in COSTUMES.get(slot, {}):
                costume_data = COSTUMES[slot][costume_id]
                # 显示装扮图标
                icon = Image(
                    source=f'assets/images/costumes/{costume_data["file"]}',
                    allow_stretch=True,
                    keep_ratio=True,
                    size_hint_y=0.6
                )
                slot_box.add_widget(icon)
                slot_box.add_widget(Label(
                    text=costume_data['name'],
                    font_size='11sp',
                    font_name='DefaultFont',
                    size_hint_y=0.2
                ))
                slot_box.add_widget(Label(
                    text=costume_data['bonus'],
                    font_size='9sp',
                    color=(0.4, 0.7, 0.4, 1),
                    font_name='DefaultFont',
                    size_hint_y=0.2
                ))
            else:
                # 空槽位
                slot_box.add_widget(Label(
                    text=f'无{CATEGORY_NAMES[slot]}',
                    font_size='11sp',
                    color=(0.6, 0.6, 0.6, 1),
                    font_name='DefaultFont'
                ))
            
            self.outfit_display.add_widget(slot_box)
    
    def show_category(self, category):
        """显示指定分类"""
        self.current_category = category
        
        # 更新按钮颜色
        for cat, btn in self.category_buttons.items():
            if cat == category:
                btn.background_color = (0.9, 0.5, 0.7, 1)
            else:
                btn.background_color = (0.75, 0.75, 0.75, 1)
        
        # 清空列表区
        self.items_area.clear_widgets()
        
        scroll = ScrollView()
        grid = GridLayout(cols=2, spacing=10, padding=10, size_hint_y=None)
        grid.bind(minimum_height=grid.setter('height'))
        
        costumes = COSTUMES.get(category, {})
        owned = game_data.get_costumes().get('owned', [])
        equipped = game_data.get_equipped_costumes().get(category)
        
        for costume_id, costume_data in costumes.items():
            is_owned = costume_id in owned
            is_equipped = equipped == costume_id
            card = self.create_costume_card(category, costume_id, costume_data, is_owned, is_equipped)
            grid.add_widget(card)
        
        scroll.add_widget(grid)
        self.items_area.add_widget(scroll)
    
    def create_costume_card(self, category, costume_id, costume_data, is_owned, is_equipped):
        """创建装扮卡片"""
        card = BoxLayout(orientation='vertical', size_hint_y=None, height=140, padding=8, spacing=4)
        
        # 背景色
        if is_equipped:
            bg_color = (0.7, 0.9, 0.7, 1)  # 绿色-已装备
        elif is_owned:
            bg_color = (0.9, 0.95, 0.9, 1)  # 浅绿-已拥有
        else:
            bg_color = (0.95, 0.95, 0.95, 1)  # 灰色-未拥有
        
        with card.canvas.before:
            Color(*bg_color)
            card.rect = Rectangle(pos=card.pos, size=card.size)
        card.bind(pos=lambda obj, val: setattr(card.rect, 'pos', val))
        card.bind(size=lambda obj, val: setattr(card.rect, 'size', val))
        
        # 装扮图标
        icon = Image(
            source=f'assets/images/costumes/{costume_data["file"]}',
            allow_stretch=True,
            keep_ratio=True,
            size_hint_y=0.4
        )
        card.add_widget(icon)
        
        # 名称
        card.add_widget(Label(
            text=costume_data['name'],
            font_size='14sp',
            bold=True,
            color=(0.2, 0.2, 0.2, 1),
            font_name='DefaultFont',
            size_hint_y=0.18
        ))
        
        # 效果
        card.add_widget(Label(
            text=costume_data['bonus'],
            font_size='11sp',
            color=(0.5, 0.5, 0.5, 1),
            font_name='DefaultFont',
            size_hint_y=0.14
        ))
        
        # 操作按钮
        if is_equipped:
            btn = Button(
                text='已装备',
                size_hint_y=0.22,
                background_color=(0.4, 0.8, 0.4, 1),
                font_name='DefaultFont',
                font_size='12sp'
            )
            btn.bind(on_press=lambda x: self.unequip(category))
        elif is_owned:
            btn = Button(
                text='装备',
                size_hint_y=0.22,
                background_color=(0.3, 0.7, 0.9, 1),
                font_name='DefaultFont',
                font_size='12sp'
            )
            btn.bind(on_press=lambda x, c=category, cid=costume_id: self.equip(c, cid))
        else:
            btn_box = BoxLayout(size_hint_y=0.22, spacing=2)
            coin_icon = Image(source='assets/images/icons/coin.png', allow_stretch=True, keep_ratio=True, size_hint_x=0.25)
            buy_btn = Button(
                text=str(costume_data['price']),
                background_color=(1, 0.84, 0, 1),
                font_name='DefaultFont',
                font_size='12sp',
                size_hint_x=0.75
            )
            buy_btn.bind(on_press=lambda x, c=category, cid=costume_id, p=costume_data['price']: self.buy(c, cid, p))
            btn_box.add_widget(coin_icon)
            btn_box.add_widget(buy_btn)
            card.add_widget(btn_box)
            return card
        
        card.add_widget(btn)
        return card
    
    def buy(self, category, costume_id, price):
        """购买装扮"""
        success, msg = game_data.buy_costume(costume_id, category, price)
        self.show_message(msg)
        if success:
            self.show_category(category)
    
    def equip(self, category, costume_id):
        """装备装扮"""
        success, msg = game_data.equip_costume(costume_id, category)
        self.show_message(msg)
        if success:
            self.show_category(category)
            self.update_outfit_display()
    
    def unequip(self, category):
        """卸下装扮"""
        success, msg = game_data.unequip_costume(category)
        self.show_message(msg)
        if success:
            self.show_category(category)
            self.update_outfit_display()
    
    def show_message(self, message):
        """显示消息"""
        popup = Popup(
            title='提示',
            content=Label(text=message, font_size='16sp', font_name='DefaultFont'),
            size_hint=(0.6, 0.25)
        )
        popup.open()
        Clock.schedule_once(lambda dt: popup.dismiss(), 1.2)
    
    def go_back(self):
        """返回首页"""
        self.manager.current = 'home'
    
    def on_enter(self):
        """进入屏幕时刷新"""
        self.update_ui(0)
        self.show_category(self.current_category)
