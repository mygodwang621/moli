[app]
# 应用标题
title = 茉莉酱的学习乐园

# 包名（小写，无空格）
package.name = molijiang

# 包域名
package.domain = com.molijiang.app

# 源文件目录
source.dir = .

# 主程序文件
source.include_exts = py,png,jpg,kv,atlas,json,ttf,ttc,otf

# 版本号
version = 1.0.0

# 依赖项
requirements = python3,kivy

# 图标（如果有的话）
# icon.filename = assets/icon.png

# 权限
android.permissions = INTERNET

# API级别
android.api = 33
android.minapi = 21
# android.sdk 和 android.ndk 已弃用，使用以下方式
# 使用环境变量或默认路径
android.ndk_path = ~/.buildozer/android/platform/android-ndk-r25b
android.sdk_path = ~/.buildozer/android/platform/android-sdk

# 架构
android.archs = armeabi-v7a,arm64-v8a

# 屏幕方向
orientation = portrait

# 全屏
fullscreen = 0

[buildozer]
# 日志级别
log_level = 2

# 构建目录
build_dir = ./.buildozer

# 打包模式（debug/release）
# mode = debug
