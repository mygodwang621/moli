import json
import os

class GameData:
    def __init__(self):
        self.data_file = "save_data.json"
        self.data = self.load_data()
    
    def load_data(self):
        """加载存档数据"""
        if os.path.exists(self.data_file):
            try:
                with open(self.data_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except:
                return self.get_default_data()
        return self.get_default_data()
    
    def get_default_data(self):
        """默认数据"""
        return {
            "coins": 100,  # 初始金币
            "pig": {
                "name": "猪小弟",
                "level": 1,
                "exp": 0,
                "hunger": 80,  # 饱食度 0-100
                "happiness": 80,  # 快乐值 0-100
                "growth": 0,  # 成长值
            },
            "inventory": {
                "foods": {"普通饲料": 3},
                "items": {}
            },
            "achievements": {
                "questions_answered": 0,
                "correct_answers": 0,
                "days_played": 1,
                "pig_level": 1
            },
            "daily_tasks": {
                "questions_today": 0,
                "last_play_date": ""
            },
            "costumes": {
                "owned": [],  # 已购买的装扮
                "equipped": {  # 当前装备的装扮
                    "hat": None,
                    "clothes": None,
                    "accessory": None
                }
            }
        }
    
    def save_data(self):
        """保存数据"""
        with open(self.data_file, 'w', encoding='utf-8') as f:
            json.dump(self.data, f, ensure_ascii=False, indent=2)
    
    def get_coins(self):
        return self.data["coins"]
    
    def add_coins(self, amount):
        self.data["coins"] += amount
        self.save_data()
    
    def spend_coins(self, amount):
        if self.data["coins"] >= amount:
            self.data["coins"] -= amount
            self.save_data()
            return True
        return False
    
    def get_pig_status(self):
        return self.data["pig"]
    
    def feed_pig(self, food_name, food_data):
        """喂养猪小弟"""
        pig = self.data["pig"]
        
        # 减少背包中的食物
        if food_name in self.data["inventory"]["foods"]:
            self.data["inventory"]["foods"][food_name] -= 1
            if self.data["inventory"]["foods"][food_name] <= 0:
                del self.data["inventory"]["foods"][food_name]
        
        # 增加饱食度和快乐值
        pig["hunger"] = min(100, pig["hunger"] + food_data["hunger"])
        pig["happiness"] = min(100, pig["happiness"] + food_data["happiness"])
        pig["growth"] += 10
        
        # 检查升级
        level_reward = self._check_level_up()
        
        self.save_data()
        return True, level_reward
    
    def use_item(self, item_name, item_data):
        """使用道具"""
        if item_name in self.data["inventory"]["items"]:
            self.data["inventory"]["items"][item_name] -= 1
            if self.data["inventory"]["items"][item_name] <= 0:
                del self.data["inventory"]["items"][item_name]
            
            pig = self.data["pig"]
            pig["happiness"] = min(100, pig["happiness"] + item_data["happiness"])
            pig["growth"] += 5
            
            level_reward = self._check_level_up()
            self.save_data()
            return True, level_reward
        return False, 0
    
    def _check_level_up(self):
        """检查是否升级"""
        pig = self.data["pig"]
        growth_needed = pig["level"] * 100
        
        if pig["growth"] >= growth_needed:
            pig["level"] += 1
            pig["growth"] = 0
            pig["hunger"] = 100
            pig["happiness"] = 100
            self.data["achievements"]["pig_level"] = pig["level"]
            
            # 升级奖励
            level_reward = pig["level"] * 50  # 每级奖励50金币
            self.data["coins"] += level_reward
            return level_reward
        return 0
    
    def add_food(self, food_name, quantity=1):
        """添加食物到背包"""
        if food_name not in self.data["inventory"]["foods"]:
            self.data["inventory"]["foods"][food_name] = 0
        self.data["inventory"]["foods"][food_name] += quantity
        self.save_data()
    
    def add_item(self, item_name, quantity=1):
        """添加道具到背包"""
        if item_name not in self.data["inventory"]["items"]:
            self.data["inventory"]["items"] = {}
        if item_name not in self.data["inventory"]["items"]:
            self.data["inventory"]["items"][item_name] = 0
        self.data["inventory"]["items"][item_name] += quantity
        self.save_data()
    
    def record_answer(self, correct=True):
        """记录答题"""
        # 确保所有键都存在（兼容旧存档）
        if "achievements" not in self.data:
            self.data["achievements"] = {}
        if "questions_answered" not in self.data["achievements"]:
            self.data["achievements"]["questions_answered"] = 0
        if "correct_answers" not in self.data["achievements"]:
            self.data["achievements"]["correct_answers"] = 0
        if "daily_tasks" not in self.data:
            self.data["daily_tasks"] = {}
        
        # 确保 daily_tasks 内的键存在
        if "questions_today" not in self.data["daily_tasks"]:
            self.data["daily_tasks"]["questions_today"] = 0
        if "last_play_date" not in self.data["daily_tasks"]:
            self.data["daily_tasks"]["last_play_date"] = ""
        
        self.data["achievements"]["questions_answered"] += 1
        if correct:
            self.data["achievements"]["correct_answers"] += 1
        self.data["daily_tasks"]["questions_today"] += 1
        self.save_data()
    
    def get_inventory(self):
        return self.data["inventory"]
    
    def get_achievements(self):
        return self.data["achievements"]
    
    # ========== 装扮系统 ==========
    def get_costumes(self):
        """获取装扮数据"""
        if "costumes" not in self.data:
            self.data["costumes"] = {
                "owned": [],
                "equipped": {"hat": None, "clothes": None, "accessory": None}
            }
            self.save_data()
        return self.data["costumes"]
    
    def buy_costume(self, costume_id, costume_type, price):
        """购买装扮"""
        costumes = self.get_costumes()
        if costume_id in costumes["owned"]:
            return False, "已经拥有这个装扮了"
        if self.data["coins"] < price:
            return False, "金币不足"
        
        self.data["coins"] -= price
        costumes["owned"].append(costume_id)
        self.save_data()
        return True, "购买成功"
    
    def equip_costume(self, costume_id, costume_type):
        """装备装扮"""
        costumes = self.get_costumes()
        if costume_id not in costumes["owned"]:
            return False, "还未拥有这个装扮"
        
        costumes["equipped"][costume_type] = costume_id
        self.save_data()
        return True, "装备成功"
    
    def unequip_costume(self, costume_type):
        """卸下装扮"""
        costumes = self.get_costumes()
        costumes["equipped"][costume_type] = None
        self.save_data()
        return True, "已卸下"
    
    def get_equipped_costumes(self):
        """获取当前装备的装扮"""
        return self.get_costumes()["equipped"]

# 全局游戏数据实例
game_data = GameData()
