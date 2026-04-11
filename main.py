from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, FadeTransition
from kivy.core.window import Window
from kivy.core.text import LabelBase
from kivy.config import Config

# 注册中文字体
LabelBase.register(name='DefaultFont', fn_regular='C:/Windows/Fonts/simhei.ttf')

# 设置窗口大小（模拟手机屏幕）
Config.set('graphics', 'width', '400')
Config.set('graphics', 'height', '700')
Window.size = (400, 700)

# 导入各个屏幕
from screens.home_screen import HomeScreen
from screens.quiz_screen import QuizScreen
from screens.pig_home_screen import PigHomeScreen
from screens.shop_screen import ShopScreen
from screens.achievements_screen import AchievementsScreen
from screens.daily_tasks_screen import DailyTasksScreen
from screens.dressup_screen import DressUpScreen
from screens.report_screen import ReportScreen
from screens.settings_screen import SettingsScreen


class MolijiangApp(App):
    """茉莉酱学习乐园 App"""
    
    def build(self):
        self.title = '茉莉酱的学习乐园'
        
        # 设置窗口背景为白色
        from kivy.core.window import Window
        Window.clearcolor = (1, 1, 1, 1)  # 白色背景
        
        # 创建屏幕管理器
        sm = ScreenManager(transition=FadeTransition())
        
        # 添加各个屏幕
        sm.add_widget(HomeScreen(name='home'))
        sm.add_widget(QuizScreen(name='quiz'))
        sm.add_widget(PigHomeScreen(name='pig_home'))
        sm.add_widget(ShopScreen(name='shop'))
        sm.add_widget(AchievementsScreen(name='achievements'))
        sm.add_widget(DailyTasksScreen(name='daily_tasks'))
        sm.add_widget(DressUpScreen(name='dressup'))
        sm.add_widget(ReportScreen(name='report'))
        sm.add_widget(SettingsScreen(name='settings'))
        
        return sm


if __name__ == '__main__':
    MolijiangApp().run()
