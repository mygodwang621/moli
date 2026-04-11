#!/usr/bin/env python3
"""
茉莉酱学习乐园 - 自测脚本
测试所有核心功能
"""

import sys
import os

# 测试1: 导入测试
def test_imports():
    print("=" * 50)
    print("测试1: 模块导入")
    print("=" * 50)
    try:
        from data.questions import QUESTIONS, FOODS, ITEMS
        from data.game_data import game_data
        from screens.home_screen import HomeScreen
        from screens.quiz_screen import QuizScreen
        from screens.pig_home_screen import PigHomeScreen
        from screens.shop_screen import ShopScreen
        from screens.achievements_screen import AchievementsScreen
        from screens.daily_tasks_screen import DailyTasksScreen
        from screens.dressup_screen import DressUpScreen
        from screens.report_screen import ReportScreen
        from screens.settings_screen import SettingsScreen
        from utils.sound_manager import sound_manager
        from ui.character_widgets import MolijiangWidget, PigWidget
        print("✓ 所有模块导入成功")
        return True
    except Exception as e:
        print(f"✗ 导入失败: {e}")
        return False

# 测试2: 题库测试
def test_questions():
    print("\n" + "=" * 50)
    print("测试2: 题库数据")
    print("=" * 50)
    try:
        from data.questions import QUESTIONS
        total = 0
        for subject, questions in QUESTIONS.items():
            count = len(questions)
            total += count
            print(f"  {subject}: {count}题")
        print(f"✓ 题库总计: {total}题")
        return True
    except Exception as e:
        print(f"✗ 题库测试失败: {e}")
        return False

# 测试3: 游戏数据测试
def test_game_data():
    print("\n" + "=" * 50)
    print("测试3: 游戏数据")
    print("=" * 50)
    try:
        from data.game_data import game_data
        
        # 测试获取数据
        coins = game_data.get_coins()
        pig = game_data.get_pig_status()
        inventory = game_data.get_inventory()
        achievements = game_data.get_achievements()
        
        print(f"  金币: {coins}")
        print(f"  猪小弟等级: {pig.get('level', 1)}")
        print(f"  背包食物: {inventory.get('foods', {})}")
        print(f"  答题数: {achievements.get('questions_answered', 0)}")
        print("✓ 游戏数据正常")
        return True
    except Exception as e:
        print(f"✗ 游戏数据测试失败: {e}")
        return False

# 测试4: 经济系统测试
def test_economy():
    print("\n" + "=" * 50)
    print("测试4: 经济系统")
    print("=" * 50)
    try:
        from data.game_data import game_data
        
        # 测试金币操作
        initial_coins = game_data.get_coins()
        game_data.add_coins(10)
        new_coins = game_data.get_coins()
        assert new_coins == initial_coins + 10, "金币添加失败"
        
        # 恢复
        game_data.spend_coins(10)
        print("✓ 金币系统正常")
        return True
    except Exception as e:
        print(f"✗ 经济系统测试失败: {e}")
        return False

# 测试5: 装扮系统测试
def test_dressup():
    print("\n" + "=" * 50)
    print("测试5: 装扮系统")
    print("=" * 50)
    try:
        from screens.dressup_screen import COSTUMES
        
        total_costumes = 0
        for category, items in COSTUMES.items():
            count = len(items)
            total_costumes += count
            print(f"  {category}: {count}件")
        print(f"✓ 装扮总计: {total_costumes}件")
        return True
    except Exception as e:
        print(f"✗ 装扮系统测试失败: {e}")
        return False

# 测试6: 每日任务测试
def test_daily_tasks():
    print("\n" + "=" * 50)
    print("测试6: 每日任务")
    print("=" * 50)
    try:
        from data.game_data import game_data
        
        daily_tasks = game_data.data.get('daily_tasks', {})
        tasks = daily_tasks.get('tasks', [])
        print(f"  任务数量: {len(tasks)}")
        for task in tasks:
            print(f"    - {task.get('title', '未知')}")
        print("✓ 每日任务系统正常")
        return True
    except Exception as e:
        print(f"✗ 每日任务测试失败: {e}")
        return False

# 测试7: 学习报告测试
def test_report():
    print("\n" + "=" * 50)
    print("测试7: 学习报告")
    print("=" * 50)
    try:
        from data.game_data import game_data
        
        achievements = game_data.get_achievements()
        pig = game_data.get_pig_status()
        
        print(f"  答题数: {achievements.get('questions_answered', 0)}")
        print(f"  正确数: {achievements.get('correct_answers', 0)}")
        print(f"  猪小弟等级: {pig.get('level', 1)}")
        print("✓ 学习报告数据正常")
        return True
    except Exception as e:
        print(f"✗ 学习报告测试失败: {e}")
        return False

# 测试8: 音效系统测试
def test_sound():
    print("\n" + "=" * 50)
    print("测试8: 音效系统")
    print("=" * 50)
    try:
        from utils.sound_manager import sound_manager
        
        # 测试音效开关
        initial = sound_manager.enabled
        sound_manager.toggle_sound()
        assert sound_manager.enabled != initial, "音效开关失败"
        sound_manager.toggle_sound()  # 恢复
        
        print(f"  音效状态: {'开启' if sound_manager.enabled else '关闭'}")
        print(f"  BGM状态: {'开启' if sound_manager.bgm_enabled else '关闭'}")
        print("✓ 音效系统正常")
        return True
    except Exception as e:
        print(f"✗ 音效系统测试失败: {e}")
        return False

# 主测试函数
def run_all_tests():
    print("\n" + "=" * 50)
    print("茉莉酱学习乐园 - 功能自测")
    print("=" * 50)
    
    tests = [
        test_imports,
        test_questions,
        test_game_data,
        test_economy,
        test_dressup,
        test_daily_tasks,
        test_report,
        test_sound,
    ]
    
    results = []
    for test in tests:
        try:
            result = test()
            results.append(result)
        except Exception as e:
            print(f"✗ 测试异常: {e}")
            results.append(False)
    
    print("\n" + "=" * 50)
    print("测试结果汇总")
    print("=" * 50)
    passed = sum(results)
    total = len(results)
    print(f"通过: {passed}/{total}")
    
    if passed == total:
        print("✓ 所有测试通过！")
        return 0
    else:
        print("✗ 部分测试失败，请检查")
        return 1

if __name__ == '__main__':
    sys.exit(run_all_tests())
