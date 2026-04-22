from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, FadeTransition
from kivy.core.window import Window
from kivy.core.text import LabelBase
from kivy.config import Config
from kivy.clock import Clock
import os
import platform

# 注册中文字体（跨平台兼容，优先使用打包内字体）
_base_dir = os.path.dirname(os.path.abspath(__file__))
_bundled_font = os.path.join(_base_dir, 'assets', 'fonts', 'simhei.ttf')

if os.path.exists(_bundled_font):
    font_path = _bundled_font
elif platform.system() == 'Windows':
    font_path = 'C:/Windows/Fonts/simhei.ttf'
else:
    font_path = None

if font_path and os.path.exists(font_path):
    LabelBase.register(name='DefaultFont', fn_regular=font_path)
    LabelBase.register(name='Roboto', fn_regular=font_path)

# 桌面端限制窗口大小
if platform.system() in ('Windows', 'Linux', 'Darwin'):
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


def _apply_android_fullscreen(*args):
    """Android 沉浸式全屏，在 UI 线程执行"""
    try:
        from android.runnable import run_on_ui_thread
        from jnius import autoclass

        @run_on_ui_thread
        def _do_fullscreen():
            View = autoclass('android.view.View')
            activity = autoclass('org.kivy.android.PythonActivity').mActivity
            window = activity.getWindow()
            decor = window.getDecorView()
            # 让窗口布局延伸到状态栏和导航栏下面
            WindowManager = autoclass('android.view.WindowManager$LayoutParams')
            flags = (View.SYSTEM_UI_FLAG_LAYOUT_STABLE |
                     View.SYSTEM_UI_FLAG_LAYOUT_HIDE_NAVIGATION |
                     View.SYSTEM_UI_FLAG_LAYOUT_FULLSCREEN |
                     View.SYSTEM_UI_FLAG_FULLSCREEN |
                     View.SYSTEM_UI_FLAG_HIDE_NAVIGATION |
                     View.SYSTEM_UI_FLAG_IMMERSIVE_STICKY)
            decor.setSystemUiVisibility(flags)
            # 同时设置窗口 flag 让内容填充状态栏区域
            window.addFlags(WindowManager.FLAG_FULLSCREEN)
            window.addFlags(WindowManager.FLAG_LAYOUT_NO_LIMITS)

        _do_fullscreen()
    except Exception:
        pass


class MolijiangApp(App):
    """茉莉酱学习乐园 App"""

    def build(self):
        self.title = '茉莉酱的学习乐园'

        # 背景色：Android 用黑色避免启动闪白屏，桌面用白色
        if platform.system() not in ('Windows', 'Linux', 'Darwin'):
            Window.clearcolor = (0, 0, 0, 1)   # Android 启动时黑色底，避免闪白
            # 立即执行一次，再延迟 0.5 秒重复确保生效
            Clock.schedule_once(_apply_android_fullscreen, 0)
            Clock.schedule_once(_apply_android_fullscreen, 0.5)
            Clock.schedule_once(_apply_android_fullscreen, 1.5)
        else:
            Window.clearcolor = (1, 1, 1, 1)

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
