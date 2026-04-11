#!/bin/bash
# 使用国内镜像加速构建

set -e

echo "===== 配置国内镜像 ====="

# 配置 git 使用国内镜像
git config --global url."https://ghproxy.com/https://github.com/".insteadOf "https://github.com/"

# 配置环境变量使用国内镜像
export PIP_INDEX_URL=https://pypi.tuna.tsinghua.edu.cn/simple
export PIP_TRUSTED_HOST=pypi.tuna.tsinghua.edu.cn

# 进入项目目录
cd /mnt/h/workspace/molijiang

# 激活虚拟环境
source venv/bin/activate

# 升级 pip 并安装依赖
pip install --upgrade pip setuptools wheel
pip install buildozer cython

echo "===== 开始构建 ====="

# 执行打包
buildozer android debug

echo "===== 构建完成 ====="
