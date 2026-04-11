# 深圳二年级下册题库
# 导入扩展题库
from data.questions_extended import QUESTIONS_EXTENDED

# 合并基础题库和扩展题库
QUESTIONS = {
    "语文": [
        {
            "question": "《咏柳》的作者是谁？",
            "options": ["李白", "贺知章", "杜甫", "白居易"],
            "answer": 1,
            "reward": 10
        },
        {
            "question": "'草长莺飞二月天'的下一句是？",
            "options": ["拂堤杨柳醉春烟", "儿童散学归来早", "忙趁东风放纸鸢", "碧玉妆成一树高"],
            "answer": 0,
            "reward": 10
        },
        {
            "question": "'快乐'的反义词是？",
            "options": ["高兴", "悲伤", "开心", "愉快"],
            "answer": 1,
            "reward": 5
        },
        {
            "question": "'认真'的近义词是？",
            "options": ["马虎", "仔细", "粗心", "随便"],
            "answer": 1,
            "reward": 5
        },
        {
            "question": "《找春天》一文中，春天像什么？",
            "options": ["害羞的小姑娘", "淘气的孩子", "慈祥的奶奶", "严厉的老师"],
            "answer": 0,
            "reward": 10
        }
    ],
    "数学": [
        {
            "question": "36 ÷ 6 = ?",
            "options": ["5", "6", "7", "8"],
            "answer": 1,
            "reward": 5
        },
        {
            "question": "7 × 8 = ?",
            "options": ["54", "56", "48", "63"],
            "answer": 1,
            "reward": 5
        },
        {
            "question": "100 厘米 = ? 米",
            "options": ["1", "10", "100", "0.1"],
            "answer": 0,
            "reward": 5
        },
        {
            "question": "一个正方形有（）条边",
            "options": ["3", "4", "5", "6"],
            "answer": 1,
            "reward": 5
        },
        {
            "question": "24 里面有（）个 8",
            "options": ["2", "3", "4", "5"],
            "answer": 1,
            "reward": 8
        },
        {
            "question": "最小的三位数是？",
            "options": ["100", "101", "111", "999"],
            "answer": 0,
            "reward": 10
        }
    ],
    "英语": [
        {
            "question": "'苹果'的英文是？",
            "options": ["Apple", "Orange", "Banana", "Grape"],
            "answer": 0,
            "reward": 5
        },
        {
            "question": "'书'的英文是？",
            "options": ["Pen", "Bag", "Book", "Desk"],
            "answer": 2,
            "reward": 5
        },
        {
            "question": "Good morning 的意思是？",
            "options": ["早上好", "晚上好", "你好", "再见"],
            "answer": 0,
            "reward": 5
        },
        {
            "question": "'红色'的英文是？",
            "options": ["Blue", "Green", "Yellow", "Red"],
            "answer": 3,
            "reward": 5
        },
        {
            "question": "How are you? 的正确回答是？",
            "options": ["I'm fine, thank you.", "Hello!", "Goodbye!", "Nice to meet you."],
            "answer": 0,
            "reward": 8
        }
    ],
    "科学": [
        {
            "question": "植物生长需要（）",
            "options": ["阳光、水、空气", "只有水", "只有阳光", "只有土壤"],
            "answer": 0,
            "reward": 8
        },
        {
            "question": "磁铁能吸引（）",
            "options": ["木头", "塑料", "铁", "纸"],
            "answer": 2,
            "reward": 8
        },
        {
            "question": "水的三种状态是？",
            "options": ["固态、液态、气态", "冷、温、热", "红、黄、蓝", "大、中、小"],
            "answer": 0,
            "reward": 10
        },
        {
            "question": "彩虹有几种颜色？",
            "options": ["5", "6", "7", "8"],
            "answer": 2,
            "reward": 8
        },
        {
            "question": "地球绕着（）转",
            "options": ["月亮", "太阳", "火星", "木星"],
            "answer": 1,
            "reward": 10
        }
    ]
}

# 食物数据
FOODS = {
    "普通饲料": {"price": 10, "hunger": 20, "happiness": 5, "icon": "[饲料]"},
    "营养饲料": {"price": 25, "hunger": 50, "happiness": 10, "icon": "[营养]"},
    "美味蛋糕": {"price": 50, "hunger": 30, "happiness": 30, "icon": "[蛋糕]"},
    "超级大餐": {"price": 100, "hunger": 100, "happiness": 50, "icon": "[大餐]"},
    "爱心便当": {"price": 80, "hunger": 60, "happiness": 40, "icon": "[便当]"}
}

# 道具数据
ITEMS = {
    "玩具球": {"price": 30, "happiness": 20, "icon": "[球]"},
    "泡泡机": {"price": 60, "happiness": 40, "icon": "[泡泡]"},
    "故事书": {"price": 40, "happiness": 25, "icon": "[书]"},
    "彩虹糖": {"price": 15, "happiness": 10, "icon": "[糖]"}
}

# 合并扩展题库
for subject in QUESTIONS_EXTENDED:
    if subject in QUESTIONS:
        QUESTIONS[subject].extend(QUESTIONS_EXTENDED[subject])
    else:
        QUESTIONS[subject] = QUESTIONS_EXTENDED[subject]
