#!/bin/bash
# APK 构建脚本

set -e

echo "===== 开始构建 APK ====="

# 进入项目目录
cd /mnt/h/workspace/molijiang

# 创建虚拟环境
echo "创建虚拟环境..."
python3 -m venv venv
source venv/bin/activate

# 安装依赖
echo "安装依赖..."
pip install -q buildozer cython

# 执行打包
echo "开始打包 APK..."
echo "y" | buildozer android debug

echo "===== 构建完成 ====="
echo "APK 文件位于: bin/"
ls -la bin/
