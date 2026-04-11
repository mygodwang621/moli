#!/bin/bash
# 手动下载依赖包脚本

set -e

echo "===== 开始手动下载依赖包 ====="

# 创建目录
mkdir -p /mnt/h/workspace/molijiang/.buildozer/android/platform/build-armeabi-v7a_arm64-v8a/packages
cd /mnt/h/workspace/molijiang/.buildozer/android/platform/build-armeabi-v7a_arm64-v8a/packages

# 定义下载函数
download_file() {
    local url=$1
    local filename=$2
    local pkg_dir=$3
    
    if [ ! -f "$pkg_dir/$filename" ]; then
        echo "下载 $filename..."
        mkdir -p "$pkg_dir"
        cd "$pkg_dir"
        wget --timeout=60 --tries=3 "$url" -O "$filename" || {
            echo "下载失败: $filename"
            return 1
        }
        cd ..
    else
        echo "$filename 已存在，跳过"
    fi
}

# 使用国内镜像下载
# Python 3.12
download_file "https://registry.npmmirror.com/-/binary/python/3.12.0/Python-3.12.0.tgz" "Python-3.12.0.tgz" "python3"

# SDL2
download_file "https://github.com/libsdl-org/SDL/releases/download/release-2.30.0/SDL2-2.30.0.tar.gz" "SDL2-2.30.0.tar.gz" "sdl2"

# SDL2_image
download_file "https://github.com/libsdl-org/SDL_image/releases/download/release-2.8.2/SDL2_image-2.8.2.tar.gz" "SDL2_image-2.8.2.tar.gz" "sdl2_image"

# SDL2_mixer
download_file "https://github.com/libsdl-org/SDL_mixer/releases/download/release-2.8.0/SDL2_mixer-2.8.0.tar.gz" "SDL2_mixer-2.8.0.tar.gz" "sdl2_mixer"

# SDL2_ttf
download_file "https://github.com/libsdl-org/SDL_ttf/releases/download/release-2.20.2/SDL2_ttf-2.20.2.tar.gz" "SDL2_ttf-2.20.2.tar.gz" "sdl2_ttf"

# FreeType
download_file "https://download.savannah.gnu.org/releases/freetype/freetype-2.13.2.tar.gz" "freetype-2.13.2.tar.gz" "freetype"

# libpng
download_file "https://downloads.sourceforge.net/project/libpng/libpng16/1.6.40/libpng-1.6.40.tar.gz" "libpng-1.6.40.tar.gz" "png"

# libjpeg
download_file "https://downloads.sourceforge.net/project/libjpeg-turbo/2.1.5.1/libjpeg-turbo-2.1.5.1.tar.gz" "libjpeg-turbo-2.1.5.1.tar.gz" "jpeg"

# libffi
download_file "https://github.com/libffi/libffi/releases/download/v3.4.4/libffi-3.4.4.tar.gz" "libffi-3.4.4.tar.gz" "libffi"

# OpenSSL
download_file "https://www.openssl.org/source/openssl-3.1.4.tar.gz" "openssl-3.1.4.tar.gz" "openssl"

# SQLite
download_file "https://www.sqlite.org/2023/sqlite-autoconf-3440200.tar.gz" "sqlite-autoconf-3440200.tar.gz" "sqlite3"

echo "===== 下载完成 ====="
echo "所有包已下载到:"
ls -la /mnt/h/workspace/molijiang/.buildozer/android/platform/build-armeabi-v7a_arm64-v8a/packages/
