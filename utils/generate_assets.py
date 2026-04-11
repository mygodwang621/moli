"""
生成游戏图片资源
使用PIL生成简单的游戏素材
"""
from PIL import Image, ImageDraw, ImageFont
import os

def ensure_dir(path):
    """确保目录存在"""
    if not os.path.exists(path):
        os.makedirs(path)

def create_molijiang_image():
    """创建茉莉酱角色图 - 动漫风格+立体感"""
    size = 400
    img = Image.new('RGBA', (size, size), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    
    cx = size // 2
    outline_color = (93, 64, 55, 255)  # 深褐色描边 #5D4037
    outline_width = 2
    
    # ========== 身体 ==========
    # 黄色连衣裙（A字型）- 立体感左亮右暗
    dress_light = (255, 235, 140, 255)
    dress_color = (255, 228, 120, 255)
    dress_dark = (240, 210, 100, 255)
    
    # 裙子主体（分三部分绘制立体感）
    draw.polygon([
        (cx-20, 200), (cx-90, 360), (cx, 360), (cx-10, 200)
    ], fill=dress_light)  # 左侧亮部
    draw.polygon([
        (cx+10, 200), (cx, 360), (cx+90, 360), (cx+20, 200)
    ], fill=dress_dark)   # 右侧暗部
    draw.polygon([
        (cx-10, 200), (cx, 360), (cx+10, 200)
    ], fill=dress_color)  # 中间
    
    # 裙子褶皱阴影
    draw.polygon([
        (cx-20, 200), (cx-40, 360), (cx-20, 360),
    ], fill=(220, 190, 80, 255))
    
    # 白色衣领（带描边）
    draw.polygon([
        (cx, 195), (cx-25, 215), (cx, 225), (cx+25, 215),
    ], fill=(255, 255, 255, 255))
    draw.line([(cx-25, 215), (cx, 225), (cx+25, 215)], fill=outline_color, width=outline_width)
    
    # 手臂（自然下垂，带立体感）
    # 左臂（亮部）
    draw.ellipse([cx-110, 220, cx-70, 280], fill=(255, 235, 140, 255), outline=outline_color, width=outline_width)
    draw.ellipse([cx-115, 270, cx-75, 310], fill=(255, 220, 200, 255), outline=outline_color, width=outline_width)
    # 右臂（暗部）
    draw.ellipse([cx+70, 220, cx+110, 280], fill=(245, 215, 100, 255), outline=outline_color, width=outline_width)
    draw.ellipse([cx+75, 270, cx+115, 310], fill=(255, 220, 200, 255), outline=outline_color, width=outline_width)
    
    # ========== 头部 ==========
    # 脸型（动漫风格瓜子脸）- 立体感左亮右暗
    face_light = (255, 225, 205, 255)
    face_shadow = (245, 210, 190, 255)
    
    # 脸部左亮部
    draw.polygon([(cx, 50), (cx-75, 80), (cx-80, 140), (cx-70, 180), (cx, 195)], fill=face_light)
    # 脸部右暗部
    draw.polygon([(cx, 50), (cx, 195), (cx+70, 180), (cx+80, 140), (cx+75, 80)], fill=face_shadow)
    
    # 脸部描边
    face_outline = [(cx, 50), (cx-75, 80), (cx-80, 140), (cx-70, 180), (cx, 195), 
                    (cx+70, 180), (cx+80, 140), (cx+75, 80)]
    for i in range(len(face_outline)):
        draw.line([face_outline[i], face_outline[(i+1) % len(face_outline)]], 
                  fill=outline_color, width=outline_width)
    
    # 头发（深棕色，带立体感）
    hair_shadow = (60, 45, 35, 255)
    hair_base = (80, 60, 50, 255)
    hair_highlight = (110, 90, 80, 255)
    
    # 后脑勺头发（暗部）
    draw.ellipse([cx-90, 30, cx+90, 120], fill=hair_shadow, outline=outline_color, width=outline_width)
    # 头顶（亮部）
    draw.ellipse([cx-70, 10, cx+70, 80], fill=hair_highlight, outline=outline_color, width=outline_width)
    
    # 刘海（带光影效果）
    for i in range(3):
        x = cx - 30 + i * 30
        draw.pieslice([x-15, 35, x+15, 85], 180, 270, fill=hair_highlight)  # 亮部
        draw.pieslice([x-15, 35, x+15, 85], 270, 360, fill=hair_base)       # 暗部
    
    # 两侧鬓角
    draw.polygon([(cx-75, 100), (cx-85, 160), (cx-70, 170), (cx-65, 120)], fill=hair_base, outline=outline_color, width=outline_width)
    draw.polygon([(cx+75, 100), (cx+85, 160), (cx+70, 170), (cx+65, 120)], fill=hair_shadow, outline=outline_color, width=outline_width)
    
    # ========== 黄帽子（立体感）==========
    hat_light = (255, 230, 80, 255)
    hat_color = (255, 215, 50, 255)
    hat_shadow = (235, 195, 40, 255)
    
    # 帽檐（左亮右暗）
    draw.ellipse([cx-100, 60, cx, 110], fill=hat_light)
    draw.ellipse([cx, 60, cx+100, 110], fill=hat_shadow)
    draw.ellipse([cx-30, 60, cx+30, 110], fill=hat_color)
    draw.ellipse([cx-100, 60, cx+100, 110], outline=outline_color, width=outline_width)
    
    # 帽顶（立体感）
    draw.ellipse([cx-60, 20, cx+60, 80], fill=hat_color, outline=outline_color, width=outline_width)
    # 帽顶高光（左上角）
    draw.ellipse([cx-45, 25, cx-5, 55], fill=(255, 245, 150, 200))
    # 红色帽带
    draw.arc([cx-95, 75, cx+95, 115], 0, 180, fill=(200, 50, 50, 255), width=5)
    
    # ========== 眼睛（立体感+高光）==========
    eye_y = 115
    
    def draw_eye_enhanced(draw, cx, cy, is_left):
        # 眼白（带描边）
        draw.ellipse([cx-20, cy-18, cx+20, cy+22], fill=(255, 255, 255, 255), outline=outline_color, width=outline_width)
        
        # 虹膜（绿色渐变效果）
        draw.ellipse([cx-13, cy-12, cx+13, cy+16], fill=(100, 200, 130, 255))
        draw.ellipse([cx-10, cy-9, cx+6, cy+10], fill=(130, 220, 160, 255))  # 亮部
        
        # 瞳孔
        draw.ellipse([cx-7, cy-6, cx+7, cy+10], fill=(40, 40, 40, 255))
        
        # 纯白高光（左上角 - 模拟反光，让眼神有神采）
        draw.ellipse([cx-12, cy-8, cx-2, cy+2], fill=(255, 255, 255, 255))
        draw.ellipse([cx-5, cy+2, cx+3, cy+8], fill=(255, 255, 255, 200))
        
        # 上眼线
        draw.arc([cx-22, cy-20, cx+22, cy+20], 30, 150, fill=outline_color, width=3)
        
        # 睫毛
        if is_left:
            draw.line([(cx-20, cy-5), (cx-28, cy-18)], fill=outline_color, width=2)
        else:
            draw.line([(cx+20, cy-5), (cx+28, cy-18)], fill=outline_color, width=2)
    
    # 左眼
    draw_eye_enhanced(draw, cx-35, eye_y, True)
    # 右眼
    draw_eye_enhanced(draw, cx+35, eye_y, False)
    
    # 眉毛（动漫细眉）
    draw.arc([cx-55, eye_y-35, cx-15, eye_y-15], 200, 340, fill=outline_color, width=2)
    draw.arc([cx+15, eye_y-35, cx+55, eye_y-15], 200, 340, fill=outline_color, width=2)
    
    # 腮红（半透明粉色圆形 - opacity 0.4，增加可爱度）
    blush_color = (255, 160, 160, 100)
    draw.ellipse([cx-75, 140, cx-35, 170], fill=blush_color)
    draw.ellipse([cx+35, 140, cx+75, 170], fill=blush_color)
    # 腮红高光
    draw.ellipse([cx-70, 145, cx-55, 158], fill=(255, 200, 200, 150))
    draw.ellipse([cx+45, 145, cx+60, 158], fill=(255, 200, 200, 150))
    
    # 嘴巴（小嘴微笑）
    draw.arc([cx-12, 155, cx+12, 175], 0, 180, fill=(220, 80, 100, 255), width=2)
    
    # ========== 腿部 ==========
    # 白色袜子（带描边）
    draw.rectangle([cx-35, 360, cx-15, 390], fill=(255, 255, 255, 255), outline=outline_color, width=outline_width)
    draw.rectangle([cx+15, 360, cx+35, 390], fill=(255, 255, 255, 255), outline=outline_color, width=outline_width)
    
    # 黑色小皮鞋（立体感）
    draw.ellipse([cx-45, 385, cx-10, 410], fill=(60, 60, 60, 255), outline=outline_color, width=outline_width)
    draw.ellipse([cx+10, 385, cx+45, 410], fill=(40, 40, 40, 255), outline=outline_color, width=outline_width)
    # 鞋头高光
    draw.ellipse([cx-35, 388, cx-20, 398], fill=(120, 120, 120, 255))
    draw.ellipse([cx+18, 388, cx+33, 398], fill=(100, 100, 100, 255))
    
    # 缩小到目标尺寸
    img = img.resize((200, 200), Image.Resampling.LANCZOS)
    
    return img

def create_pig_image(mood='normal'):
    """创建猪小弟角色图 - 粉色可爱小猪风格+立体感"""
    colors = {
        'normal': (255, 192, 203, 255),   # 正常 - 粉色
        'happy': (255, 218, 185, 255),    # 开心 - 桃色
        'hungry': (220, 220, 220, 255),   # 饿 - 浅灰
        'excited': (255, 182, 193, 255),  # 兴奋 - 浅粉
    }
    
    color = colors.get(mood, colors['normal'])
    outline_color = (93, 64, 55, 255)  # 深褐色描边 #5D4037
    outline_width = 2
    
    img = Image.new('RGBA', (200, 200), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    
    # 身体（立体感 - 左亮右暗）
    # 左侧亮部
    draw.ellipse([25, 50, 100, 170], fill=(min(255, color[0]+15), min(255, color[1]+15), min(255, color[2]+15), 255))
    # 右侧暗部
    draw.ellipse([100, 50, 175, 170], fill=(max(0, color[0]-15), max(0, color[1]-15), max(0, color[2]-15), 255))
    # 中间主体
    draw.ellipse([50, 50, 150, 170], fill=color)
    # 身体描边
    draw.ellipse([25, 50, 175, 170], outline=outline_color, width=outline_width)
    
    # 可爱的耳朵（半圆形，带立体感）
    ear_color = (color[0]-15, color[1]-15, color[2]-15, 255)
    draw.pieslice([35, 25, 65, 65], 0, 180, fill=ear_color, outline=outline_color, width=outline_width)
    draw.pieslice([135, 25, 165, 65], 0, 180, fill=ear_color, outline=outline_color, width=outline_width)
    # 耳朵内侧（亮部）
    draw.pieslice([40, 35, 60, 55], 0, 180, fill=(255, 220, 230, 255))
    draw.pieslice([140, 35, 160, 55], 0, 180, fill=(255, 220, 230, 255))
    
    # 眼睛（大大的可爱眼睛+高光）
    if mood == 'hungry':
        # 困倦的眼睛（弧线）
        draw.arc([55, 75, 75, 95], 0, 180, fill=outline_color, width=3)
        draw.arc([125, 75, 145, 95], 0, 180, fill=outline_color, width=3)
    else:
        # 大眼睛（带描边）
        draw.ellipse([55, 75, 75, 95], fill=(60, 40, 40, 255), outline=outline_color, width=outline_width)
        draw.ellipse([125, 75, 145, 95], fill=(60, 40, 40, 255), outline=outline_color, width=outline_width)
        # 纯白高光（左上角 - 模拟反光）
        draw.ellipse([57, 77, 64, 84], fill=(255, 255, 255, 255))
        draw.ellipse([127, 77, 134, 84], fill=(255, 255, 255, 255))
        # 小高光
        draw.ellipse([60, 80, 63, 83], fill=(255, 255, 255, 200))
        draw.ellipse([130, 80, 133, 83], fill=(255, 255, 255, 200))
    
    # 猪鼻子（椭圆形，立体感）
    nose_color = (255, 160, 170, 255)
    draw.ellipse([85, 105, 115, 125], fill=nose_color, outline=outline_color, width=outline_width)
    # 鼻孔
    draw.ellipse([92, 112, 98, 118], fill=(100, 50, 50, 255))
    draw.ellipse([102, 112, 108, 118], fill=(100, 50, 50, 255))
    
    # 嘴巴（微笑）
    if mood == 'happy' or mood == 'excited':
        # 开心的大笑
        draw.arc([85, 115, 115, 145], 0, 180, fill=(200, 80, 100, 255), width=3)
        # 舌头
        draw.ellipse([95, 135, 105, 145], fill=(255, 150, 150, 255))
    else:
        # 普通微笑
        draw.arc([90, 120, 110, 140], 0, 180, fill=(200, 80, 100, 255), width=2)
    
    # 腮红（半透明粉色圆形 - opacity 0.4）
    blush_color = (255, 160, 170, 100)
    draw.ellipse([35, 95, 60, 120], fill=blush_color)
    draw.ellipse([140, 95, 165, 120], fill=blush_color)
    # 腮红高光
    draw.ellipse([40, 100, 50, 110], fill=(255, 200, 210, 150))
    draw.ellipse([145, 100, 155, 110], fill=(255, 200, 210, 150))
    
    # 小短腿（带立体感）
    leg_color = (color[0]-10, color[1]-10, color[2]-10, 255)
    draw.ellipse([60, 165, 80, 185], fill=leg_color, outline=outline_color, width=outline_width)
    draw.ellipse([120, 165, 140, 185], fill=leg_color, outline=outline_color, width=outline_width)
    
    # 尾巴（卷曲，带描边）
    draw.arc([160, 100, 190, 140], 180, 360, fill=(color[0]-20, color[1]-20, color[2]-20, 255), width=3)
    
    return img

def create_food_icon(food_type):
    """创建精美的食物图标"""
    img = Image.new('RGBA', (64, 64), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    
    if food_type == 'feed':
        # 普通饲料 - 精美的饲料袋
        # 袋子主体
        draw.polygon([(15, 20), (49, 20), (52, 50), (12, 50)], fill=(160, 120, 80, 255))
        # 袋子顶部
        draw.polygon([(15, 20), (32, 10), (49, 20)], fill=(180, 140, 100, 255))
        # 标签
        draw.rectangle([22, 28, 42, 42], fill=(255, 255, 220, 255))
        draw.line([26, 35, 38, 35], fill=(100, 80, 60, 255), width=2)
    elif food_type == 'apple':
        # 红苹果 - 带光泽
        # 苹果主体
        draw.ellipse([12, 15, 52, 55], fill=(255, 60, 60, 255))
        # 高光
        draw.ellipse([18, 22, 28, 32], fill=(255, 150, 150, 180))
        # 梗
        draw.rectangle([30, 8, 34, 18], fill=(120, 80, 40, 255))
        # 叶子
        draw.ellipse([34, 5, 46, 15], fill=(80, 180, 80, 255))
    elif food_type == 'cake':
        # 精美蛋糕
        # 蛋糕底层
        draw.rectangle([10, 35, 54, 55], fill=(255, 220, 180, 255))
        # 蛋糕顶层
        draw.rectangle([14, 25, 50, 40], fill=(255, 200, 200, 255))
        # 奶油装饰
        draw.ellipse([20, 18, 30, 28], fill=(255, 255, 255, 255))
        draw.ellipse([34, 20, 44, 30], fill=(255, 255, 255, 255))
        # 樱桃
        draw.ellipse([28, 12, 36, 20], fill=(220, 30, 30, 255))
    elif food_type == 'meal':
        # 超级大餐 - 烤鸡
        # 盘子
        draw.ellipse([5, 30, 59, 60], fill=(240, 240, 240, 255))
        # 烤鸡身体
        draw.ellipse([15, 20, 49, 48], fill=(255, 180, 80, 255))
        # 鸡腿
        draw.ellipse([42, 25, 58, 40], fill=(255, 160, 60, 255))
        # 高光
        draw.ellipse([22, 28, 32, 35], fill=(255, 220, 150, 200))
    elif food_type == 'bento':
        # 爱心便当
        # 便当盒
        draw.rounded_rectangle([8, 15, 56, 55], radius=5, fill=(220, 80, 80, 255))
        # 内部白色
        draw.rounded_rectangle([12, 20, 52, 50], radius=3, fill=(255, 255, 255, 255))
        # 爱心饭团
        draw.polygon([(32, 25), (22, 32), (22, 38), (32, 45), (42, 38), (42, 32)], fill=(255, 255, 220, 255))
        # 配菜
        draw.ellipse([15, 40, 25, 48], fill=(100, 180, 100, 255))
        draw.rectangle([38, 40, 48, 48], fill=(255, 180, 100, 255))
    
    return img

def create_item_icon(item_type):
    """创建道具图标"""
    img = Image.new('RGBA', (64, 64), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    
    if item_type == 'ball':
        # 玩具球
        draw.ellipse([8, 8, 56, 56], fill=(255, 100, 100, 255), outline=(200, 50, 50, 255), width=2)
        draw.arc([15, 15, 49, 49], 45, 225, fill=(255, 255, 255, 200), width=3)
    elif item_type == 'bubble':
        # 泡泡机
        draw.rectangle([20, 30, 44, 55], fill=(100, 150, 255, 255))
        draw.ellipse([15, 10, 49, 35], fill=(200, 230, 255, 200))
        draw.ellipse([20, 0, 35, 15], fill=(220, 240, 255, 150))
    elif item_type == 'book':
        # 故事书
        draw.rectangle([10, 8, 54, 56], fill=(100, 80, 60, 255))
        draw.rectangle([14, 12, 50, 52], fill=(255, 255, 240, 255))
        draw.line([32, 15, 32, 49], fill=(200, 200, 200, 255), width=1)
    
    return img

def create_background():
    """创建游戏背景"""
    img = Image.new('RGB', (800, 600), (135, 206, 235))  # 天蓝色背景
    draw = ImageDraw.Draw(img)
    
    # 草地
    draw.rectangle([0, 400, 800, 600], fill=(100, 200, 100))
    
    # 云朵
    for x, y in [(100, 80), (300, 120), (600, 60)]:
        draw.ellipse([x, y, x+60, y+40], fill=(255, 255, 255, 200))
        draw.ellipse([x+30, y-10, x+90, y+30], fill=(255, 255, 255, 200))
    
    # 太阳
    draw.ellipse([650, 30, 750, 130], fill=(255, 220, 100))
    
    return img

def create_button_icon(button_type):
    """创建按钮图标"""
    img = Image.new('RGBA', (80, 80), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    
    # 圆形背景
    colors = {
        'study': (100, 150, 255, 255),    # 蓝色-学习
        'home': (255, 150, 100, 255),     # 橙色-家
        'shop': (100, 200, 100, 255),     # 绿色-商店
        'report': (255, 200, 100, 255),   # 黄色-报告
        'tasks': (200, 100, 200, 255),    # 紫色-任务
        'dressup': (255, 150, 150, 255),  # 粉色-装扮
        'settings': (150, 150, 150, 255), # 灰色-设置
    }
    
    color = colors.get(button_type, (150, 150, 150, 255))
    
    # 绘制圆形背景
    draw.ellipse([5, 5, 75, 75], fill=color, outline=(255, 255, 255, 200), width=3)
    
    # 绘制简单图标
    if button_type == 'study':
        # 书本图标
        draw.rectangle([25, 25, 55, 60], fill=(255, 255, 255, 255))
        draw.line([40, 25, 40, 60], fill=(100, 150, 255, 255), width=2)
    elif button_type == 'home':
        # 房子图标
        draw.polygon([(40, 20), (20, 40), (60, 40)], fill=(255, 255, 255, 255))
        draw.rectangle([28, 40, 52, 65], fill=(255, 255, 255, 255))
    elif button_type == 'shop':
        # 购物袋图标
        draw.rectangle([25, 30, 55, 60], fill=(255, 255, 255, 255))
        draw.arc([30, 20, 50, 35], 0, 180, fill=(255, 255, 255, 255), width=3)
    elif button_type == 'report':
        # 图表图标
        draw.rectangle([25, 25, 55, 60], outline=(255, 255, 255, 255), width=3)
        draw.line([30, 50, 38, 40, 45, 48, 52, 35], fill=(255, 255, 255, 255), width=3)
    elif button_type == 'tasks':
        # 任务清单图标
        draw.rectangle([25, 20, 55, 65], fill=(255, 255, 255, 255))
        for y in [30, 40, 50]:
            draw.rectangle([30, y, 35, y+3], fill=(200, 100, 200, 255))
            draw.line([40, y+1, 50, y+1], fill=(200, 100, 200, 255), width=2)
    elif button_type == 'dressup':
        # 衣服图标
        draw.polygon([(40, 20), (25, 35), (30, 65), (50, 65), (55, 35)], fill=(255, 255, 255, 255))
    elif button_type == 'settings':
        # 齿轮图标
        draw.ellipse([30, 30, 50, 50], fill=(255, 255, 255, 255))
        draw.ellipse([35, 35, 45, 45], fill=(150, 150, 150, 255))
    
    return img

def create_nav_icon(icon_type):
    """创建导航图标（返回、下一题等）"""
    img = Image.new('RGBA', (64, 64), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    
    if icon_type == 'back':
        # 返回箭头（左箭头）
        draw.polygon([(45, 15), (20, 32), (45, 49)], fill=(255, 255, 255, 255))
        draw.line([(20, 32), (50, 32)], fill=(255, 255, 255, 255), width=4)
    elif icon_type == 'next':
        # 下一题箭头（右箭头）
        draw.polygon([(19, 15), (44, 32), (19, 49)], fill=(255, 255, 255, 255))
        draw.line([(14, 32), (44, 32)], fill=(255, 255, 255, 255), width=4)
    
    return img

def create_costume_icon(costume_type, costume_name):
    """创建装扮道具图标"""
    img = Image.new('RGBA', (80, 80), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    
    # 背景框
    draw.rounded_rectangle([5, 5, 75, 75], radius=8, fill=(255, 255, 255, 200), outline=(200, 200, 200, 255), width=2)
    
    if costume_type == 'hat':
        if costume_name == '小礼帽':
            # 黑色礼帽
            draw.rectangle([25, 45, 55, 60], fill=(40, 40, 40, 255))
            draw.rectangle([20, 58, 60, 65], fill=(40, 40, 40, 255))
            draw.rectangle([28, 50, 52, 55], fill=(150, 50, 50, 255))  # 红带子
        elif costume_name == '太阳帽':
            # 黄色太阳帽
            draw.ellipse([15, 50, 65, 70], fill=(255, 220, 80, 255))
            draw.ellipse([25, 35, 55, 55], fill=(255, 200, 60, 255))
        elif costume_name == '皇冠':
            # 金色皇冠
            draw.polygon([(20, 55), (25, 35), (35, 45), (40, 30), (45, 45), (55, 35), (60, 55)], fill=(255, 215, 0, 255))
            draw.ellipse([38, 28, 42, 32], fill=(255, 50, 50, 255))  # 红宝石
        elif costume_name == '学生帽':
            # 蓝色学生帽
            draw.ellipse([20, 50, 60, 65], fill=(60, 100, 180, 255))
            draw.rectangle([30, 40, 50, 52], fill=(60, 100, 180, 255))
    
    elif costume_type == 'clothes':
        if costume_name == '小背心':
            # 红色背心
            draw.polygon([(30, 25), (50, 25), (55, 60), (25, 60)], fill=(220, 80, 80, 255))
            draw.rectangle([38, 25, 42, 60], fill=(255, 220, 200, 255))  # 开口
        elif costume_name == '运动服':
            # 蓝色运动服
            draw.polygon([(28, 22), (52, 22), (55, 62), (25, 62)], fill=(80, 150, 220, 255))
            draw.line([(40, 22), (40, 62)], fill=(255, 255, 255, 255), width=2)
        elif costume_name == '礼服':
            # 黑色礼服
            draw.polygon([(28, 22), (52, 22), (55, 62), (25, 62)], fill=(50, 50, 50, 255))
            draw.polygon([(38, 30), (42, 30), (40, 50)], fill=(255, 255, 255, 255))  # 领结
        elif costume_name == '校服':
            # 白色校服
            draw.polygon([(28, 22), (52, 22), (55, 62), (25, 62)], fill=(255, 255, 255, 255))
            draw.rectangle([38, 22, 42, 62], fill=(200, 50, 50, 255))  # 红领巾
    
    elif costume_type == 'accessory':
        if costume_name == '领结':
            # 红色领结
            draw.polygon([(25, 40), (40, 35), (40, 45)], fill=(220, 60, 60, 255))
            draw.polygon([(55, 40), (40, 35), (40, 45)], fill=(220, 60, 60, 255))
            draw.ellipse([37, 37, 43, 43], fill=(255, 100, 100, 255))
        elif costume_name == '眼镜':
            # 黑框眼镜
            draw.ellipse([20, 35, 38, 50], outline=(50, 50, 50, 255), width=3)
            draw.ellipse([42, 35, 60, 50], outline=(50, 50, 50, 255), width=3)
            draw.line([(38, 42), (42, 42)], fill=(50, 50, 50, 255), width=2)
        elif costume_name == '铃铛':
            # 金色铃铛
            draw.ellipse([25, 30, 55, 55], fill=(255, 215, 0, 255))
            draw.ellipse([35, 50, 45, 55], fill=(200, 170, 0, 255))
        elif costume_name == '围巾':
            # 红色围巾
            draw.rectangle([20, 35, 60, 50], fill=(220, 80, 80, 255))
            draw.rectangle([45, 45, 55, 65], fill=(220, 80, 80, 255))
    
    return img

def create_coin_icon():
    """创建金币图标"""
    img = Image.new('RGBA', (32, 32), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    draw.ellipse([2, 2, 30, 30], fill=(255, 215, 0, 255), outline=(255, 180, 0, 255), width=2)
    draw.text((10, 8), "¥", fill=(255, 140, 0, 255))
    return img

def create_heart_icon():
    """创建爱心图标"""
    img = Image.new('RGBA', (32, 32), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    # 简化的爱心形状
    draw.polygon([(16, 28), (4, 16), (4, 10), (10, 4), (16, 10), (22, 4), (28, 10), (28, 16)], fill=(255, 100, 100, 255))
    return img

def create_meat_icon():
    """创建肉/食物图标"""
    img = Image.new('RGBA', (32, 32), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    # 肉骨头形状
    draw.ellipse([5, 10, 27, 22], fill=(200, 100, 80, 255))
    draw.ellipse([2, 8, 10, 16], fill=(255, 255, 255, 200))
    draw.ellipse([22, 16, 30, 24], fill=(255, 255, 255, 200))
    return img

def generate_all_assets():
    """生成所有资源"""
    base_path = "assets/images"
    ensure_dir(base_path)
    ensure_dir(f"{base_path}/characters")
    ensure_dir(f"{base_path}/foods")
    ensure_dir(f"{base_path}/items")
    ensure_dir(f"{base_path}/backgrounds")
    ensure_dir(f"{base_path}/buttons")
    ensure_dir(f"{base_path}/icons")
    
    print("生成角色图片...")
    create_molijiang_image().save(f"{base_path}/characters/molijiang.png")
    create_pig_image('normal').save(f"{base_path}/characters/pig_normal.png")
    create_pig_image('happy').save(f"{base_path}/characters/pig_happy.png")
    create_pig_image('hungry').save(f"{base_path}/characters/pig_hungry.png")
    create_pig_image('excited').save(f"{base_path}/characters/pig_excited.png")
    
    print("生成食物图标...")
    create_food_icon('feed').save(f"{base_path}/foods/feed.png")
    create_food_icon('apple').save(f"{base_path}/foods/apple.png")
    create_food_icon('cake').save(f"{base_path}/foods/cake.png")
    create_food_icon('meal').save(f"{base_path}/foods/meal.png")
    create_food_icon('bento').save(f"{base_path}/foods/bento.png")
    
    print("生成道具图标...")
    create_item_icon('ball').save(f"{base_path}/items/ball.png")
    create_item_icon('bubble').save(f"{base_path}/items/bubble.png")
    create_item_icon('book').save(f"{base_path}/items/book.png")
    
    print("生成背景图...")
    create_background().save(f"{base_path}/backgrounds/home_bg.png")
    
    print("生成按钮图标...")
    create_button_icon('study').save(f"{base_path}/buttons/study.png")
    create_button_icon('home').save(f"{base_path}/buttons/home.png")
    create_button_icon('shop').save(f"{base_path}/buttons/shop.png")
    create_button_icon('report').save(f"{base_path}/buttons/report.png")
    create_button_icon('tasks').save(f"{base_path}/buttons/tasks.png")
    create_button_icon('dressup').save(f"{base_path}/buttons/dressup.png")
    create_button_icon('settings').save(f"{base_path}/buttons/settings.png")
    
    print("生成导航图标...")
    create_nav_icon('back').save(f"{base_path}/buttons/back.png")
    create_nav_icon('next').save(f"{base_path}/buttons/next.png")
    
    print("生成金币图标...")
    create_coin_icon().save(f"{base_path}/icons/coin.png")
    create_heart_icon().save(f"{base_path}/icons/heart.png")
    create_meat_icon().save(f"{base_path}/icons/meat.png")
    
    print("生成装扮图标...")
    ensure_dir(f"{base_path}/costumes")
    # 帽子
    create_costume_icon('hat', '小礼帽').save(f"{base_path}/costumes/hat_bowler.png")
    create_costume_icon('hat', '太阳帽').save(f"{base_path}/costumes/hat_sun.png")
    create_costume_icon('hat', '皇冠').save(f"{base_path}/costumes/hat_crown.png")
    create_costume_icon('hat', '学生帽').save(f"{base_path}/costumes/hat_student.png")
    # 衣服
    create_costume_icon('clothes', '小背心').save(f"{base_path}/costumes/clothes_vest.png")
    create_costume_icon('clothes', '运动服').save(f"{base_path}/costumes/clothes_sport.png")
    create_costume_icon('clothes', '礼服').save(f"{base_path}/costumes/clothes_formal.png")
    create_costume_icon('clothes', '校服').save(f"{base_path}/costumes/clothes_uniform.png")
    # 配饰
    create_costume_icon('accessory', '领结').save(f"{base_path}/costumes/acc_bowtie.png")
    create_costume_icon('accessory', '眼镜').save(f"{base_path}/costumes/acc_glasses.png")
    create_costume_icon('accessory', '铃铛').save(f"{base_path}/costumes/acc_bell.png")
    create_costume_icon('accessory', '围巾').save(f"{base_path}/costumes/acc_scarf.png")
    
    print("✅ 所有图片资源生成完成！")

if __name__ == "__main__":
    generate_all_assets()
