#!/bin/bash
# WSL 代理配置脚本

# 获取 Windows 主机 IP（WSL 2）
WINDOWS_IP=$(cat /etc/resolv.conf | grep nameserver | awk '{print $2}')

echo "Windows 主机 IP: $WINDOWS_IP"

# 配置代理（假设 VPN 端口为 7890，如果不是请修改）
PROXY_PORT=7890

export http_proxy="http://${WINDOWS_IP}:${PROXY_PORT}"
export https_proxy="http://${WINDOWS_IP}:${PROXY_PORT}"
export HTTP_PROXY="http://${WINDOWS_IP}:${PROXY_PORT}"
export HTTPS_PROXY="http://${WINDOWS_IP}:${PROXY_PORT}"

# 配置 git 代理
git config --global http.proxy "http://${WINDOWS_IP}:${PROXY_PORT}"
git config --global https.proxy "http://${WINDOWS_IP}:${PROXY_PORT}"

echo "代理已配置:"
echo "http_proxy=$http_proxy"
echo "https_proxy=$https_proxy"
git config --global --list | grep proxy
