import socket
import concurrent.futures
import random
import re
import requests
from datetime import datetime, timedelta

# --- 配置信息 ---
DOMAIN = "url.cdnhs.store"
# 按照你的要求：加上引号和逗号，且删除了源文件 cvs_mylive.txt
TARGET_FILE_LIST = ["total_live.txt", "private_only.txt", "monitor_live.txt"]

# 【核心】监控 280 和 002 两个仓库的地址
MONITOR_SOURCES = [
    "https://raw.githubusercontent.com/attypd/yipbku280/main/cvs_mylive.txt",
    "https://raw.githubusercontent.com/attypd/yipbku002/main/cvs_mylive.txt"
]

def check_port(port):
    """TCP 探测逻辑"""
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
    with concurrent.futures.ThreadPoolExecutor(max_workers=120) as executor:
        future_to_port = {executor.submit(check_port, p): p for p in port_list}
        for future in concurrent.futures.as_completed(future_to_port):
            result = future.result()
            if result:
                executor.shutdown(wait=False, cancel_futures=True)
                return result
    return None

def get_latest_port():
    """全频段扫描策略：监控优先，失败则扫全频段"""
    # 1. 优先监控主力仓库（280 和 002）
    for url in MONITOR_SOURCES:
        try:
            resp = requests.get(url, timeout=5)
            if resp.status_code == 200:
                match = re.search(rf'{re.escape(DOMAIN)}:(\d+)', resp.text)
                if match and check_port(match.group(1)):
                    print(f"Syncing from monitor source...")
                    return match.group(1)
        except:
            continue

    print(f"Starting full range scan for {DOMAIN}...")
    
    # Stage 1: 核心高位区 (40000-50000)
    res = run_scanner(list(range(40000, 50001)))
    if res: return res

    # Stage 2: 扩展高位区 (30000-40000 & 50001-65535)
    ext_list = list(range(30000, 40000)) + list(range(50001, 65536))
    random.shuffle(ext_list)
    res = run_scanner(ext_list)
    if res: return res

    # Stage 3: 中位区间 (8000-30000) - 包含你要求的 8000 到 3万
    res = run_scanner(list(range(8000, 30000)))
    if res: return res

    # Stage 4: 低位区间 (1024-8000) - 包含 3000 以下
    res = run_scanner(list(range(1024, 8000)))
    
    return res if res else "48559" # 最终保底

def update_files():
    active_port = get_latest_port()
    print(f"Active Port: {active_port}")

    # 只读源文件内容，不写回源文件
    try:
        with open("cvs_mylive.txt", 'r', encoding='utf-8') as f:
            lines = f.readlines()
    except FileNotFoundError:
        print("cvs_mylive.txt not found!")
        return

    # 内存中生成替换后的内容
    new_lines = [re.sub(rf'({re.escape(DOMAIN)}):(\d+)', f'\\1:{active_port}', line) if DOMAIN in line else line for line in lines]

    # 将结果写入目标输出文件
    for file_path in TARGET_FILE_LIST:
        try:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.writelines(new_lines)
            print(f"Successfully updated: {file_path}")
        except Exception as e:
            print(f"Failed to update {file_path}: {e}")
            
    print("Update Completed. Source file remains untouched.")

if __name__ == "__main__":
    update_files()
