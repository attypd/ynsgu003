import socket
import concurrent.futures
import random
import re
import requests
from datetime import datetime, timedelta

# --- 配置信息 ---
DOMAIN = "url.cdnhs.store"
# 仅输出这两个文件
TARGET_FILES = ["cvs_mylive.txt", "monitor_live.txt"]

# 监控 280 和 002
MONITOR_SOURCES = [
    "https://raw.githubusercontent.com/attypd/yipbku280/main/cvs_mylive.txt",
    "https://raw.githubusercontent.com/attypd/yipbku002/main/cvs_mylive.txt"
]

def check_port(port):
    """底层 TCP 探测"""
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.settimeout(0.7) 
            if s.connect_ex((DOMAIN, int(port))) == 0:
                return str(port)
    except:
        pass
    return None

def run_scanner(port_list):
    """并发扫描逻辑"""
    # 线程调优为 120，平衡速度与稳定性
    with concurrent.futures.ThreadPoolExecutor(max_workers=120) as executor:
        future_to_port = {executor.submit(check_port, p): p for p in port_list}
        for future in concurrent.futures.as_completed(future_to_port):
            result = future.result()
            if result:
                executor.shutdown(wait=False, cancel_futures=True)
                return result
    return None

def get_latest_port():
    """全频段扫描策略"""
    # 1. 优先监控主力仓库
    for url in MONITOR_SOURCES:
        try:
            resp = requests.get(url, timeout=5)
            match = re.search(rf'{re.escape(DOMAIN)}:(\d+)', resp.text)
            if match and check_port(match.group(1)):
                return match.group(1)
        except:
            continue

    print(f"Monitoring failed. Starting full range scan for {DOMAIN}...")
    
    # 2. 三阶段扫描策略
    # Stage 1: 核心区 (40000-50000)
    res = run_scanner(list(range(40000, 50001)))
    if res: return res

    # Stage 2: 扩展区 (30000-40000 & 50001-65535) 随机化扫描
    ext_list = list(range(30000, 40000)) + list(range(50001, 65536))
    random.shuffle(ext_list)
    res = run_scanner(ext_list)
    if res: return res

    # Stage 3: 低频区 (8000-30000)
    res = run_scanner(list(range(8000, 30000)))
    return res if res else "48559" # 最终保底

def update_files():
    active_port = get_latest_port()
    # 匹配图片中的 Active Port 输出
    print(f"Active Port: {active_port}")

    for file_path in TARGET_FILES:
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                lines = f.readlines()
            
            # 只修改包含特定域名的行
            new_lines = [re.sub(rf'({re.escape(DOMAIN)}):(\d+)', f'\\1:{active_port}', line) if DOMAIN in line else line for line in lines]
            
            with open(file_path, 'w', encoding='utf-8') as f:
                f.writelines(new_lines)
        except FileNotFoundError:
            pass
    print("Update Completed.") #

if __name__ == "__main__":
    update_files()
