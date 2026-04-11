"""
音效管理器
由于资源限制，目前使用print模拟音效
后续可以替换为真实的音频文件
"""

class SoundManager:
    """音效管理器"""
    
    # 音效类型
    SOUNDS = {
        'correct': '答对音效',
        'wrong': '答错音效',
        'click': '点击音效',
        'coin': '获得金币',
        'level_up': '升级音效',
        'feed': '喂养音效',
        'play': '玩耍音效',
        'buy': '购买音效',
        'complete': '完成任务',
        'bgm': '背景音乐'
    }
    
    def __init__(self):
        self.enabled = True  # 音效开关
        self.bgm_enabled = False  # 背景音乐开关
    
    def play(self, sound_name):
        """播放音效"""
        if not self.enabled:
            return
        
        if sound_name in self.SOUNDS:
            # 实际项目中这里会播放音频文件
            # 例如: self._play_audio(f'assets/sounds/{sound_name}.wav')
            print(f"[音效] {self.SOUNDS[sound_name]}")
    
    def play_correct(self):
        """播放答对音效"""
        self.play('correct')
    
    def play_wrong(self):
        """播放答错音效"""
        self.play('wrong')
    
    def play_click(self):
        """播放点击音效"""
        self.play('click')
    
    def play_coin(self):
        """播放获得金币音效"""
        self.play('coin')
    
    def play_level_up(self):
        """播放升级音效"""
        self.play('level_up')
    
    def play_feed(self):
        """播放喂养音效"""
        self.play('feed')
    
    def play_play(self):
        """播放玩耍音效"""
        self.play('play')
    
    def play_buy(self):
        """播放购买音效"""
        self.play('buy')
    
    def play_complete(self):
        """播放完成任务音效"""
        self.play('complete')
    
    def toggle_sound(self):
        """切换音效开关"""
        self.enabled = not self.enabled
        return self.enabled
    
    def toggle_bgm(self):
        """切换背景音乐"""
        self.bgm_enabled = not self.bgm_enabled
        if self.bgm_enabled:
            print("[背景音乐] 开始播放")
        else:
            print("[背景音乐] 停止播放")
        return self.bgm_enabled


# 全局音效管理器实例
sound_manager = SoundManager()
