import requests
import concurrent.futures
import re
import random
from datetime import datetime, timedelta

# --- 监控配置 ---
DOMAIN = "url.cdnhs.store"
# 监控的目标仓库 RAW 地址 (替换为你的 GitHub 用户名)
TARGET_REPOS = {
    "002": "https://raw.githubusercontent.com/attypd/shyi002/main/total_live.txt",
    "280": "https://raw.githubusercontent.com/attypd/yipbku280/main/total_live.txt"
}
SOURCE_FILE = "cvs_mylive.txt"  # 监控仓库本地也存一份源模版
TOTAL_FILE = "monitor_live.txt"
PRIVATE_FILE = "private_only.txt"

def check_port(port):
    """三段式扫描基础：探测端口存活"""
    test_url = f"http://{DOMAIN}:{port}/mytv.php?id=3"
    try:
        res = requests.head(test_url, timeout=1.5, allow_redirects=False)
        if res.status_code in [200, 302]:
            return str(port)
    except:
        return None
    return None

def run_scanner(port_list):
    """高并发随机扫描"""
    random.shuffle(port_list)
    with concurrent.futures.ThreadPoolExecutor(max_workers=100) as executor:
        future_to_port = {executor.submit(check_port, p): p for p in port_list}
        for future in concurrent.futures.as_completed(future_to_port):
            result = future.result()
            if result:
                executor.shutdown(wait=False, cancel_futures=True)
                return result
    return None

def get_emergency_port():
    """三段式紧急扫描逻辑"""
    # 第一段：40k-50k (核心)
    res = run_scanner(list(range(40000, 50001)))
    if res: return res
    
    # 第二段：30k-40k & 50k-65k (常规)
    reg_list = list(range(30000, 40000)) + list(range(50001, 65536))
    res = run_scanner(reg_list)
    if res: return res
    
    # 第三段：8k-30k (低位保底)
    res = run_scanner(list(range(8000, 30000)))
    return res if res else "48559"

def check_repo_health():
    """检查 002 和 280 仓库的健康状态"""
    now = datetime.utcnow() + timedelta(hours=8)
    for name, url in TARGET_REPOS.items():
        try:
            r = requests.get(url, timeout=5)
            if r.status_code != 200: return False
            
            # 解析时间标签: # Auto-Sync: 2026-02-20 10:30:25
            match = re.search(r'Auto-Sync: (\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2})', r.text)
            if match:
                sync_time = datetime.strptime(match.group(1), '%Y-%m-%d %H:%M:%S')
                # 如果延迟超过 20 分钟，判定为不健康
                if (now - sync_time).total_seconds() > 1200:
                    print(f"Repo {name} delay detected!")
                    return False
        except:
            return False
    return True

def do_update():
    """执行本地紧急对时并生成文件"""
    active_port = get_emergency_port()
    sync_time = (datetime.utcnow() + timedelta(hours=8)).strftime('%Y-%m-%d %H:%M:%S')
    
    total_data, private_data = [], []
    is_private_section = False
    
    try:
        with open(SOURCE_FILE, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if not line: continue
                # --- 精准替换：只改主服务器，不碰其他 ---
                if DOMAIN in line:
                    line = re.sub(rf'({re.escape(DOMAIN)}):(\d+)', f'\\1:{active_port}', line)
                
                total_data.append(line)
                if "私密频道" in line: is_private_section = True
                if is_private_section: private_data.append(line)
                
        # 生成两个文件
        with open(TOTAL_FILE, "w", encoding="utf-8") as f:
            f.write("\n".join(total_data) + f"\n\n# Emergency-Sync: {sync_time}")
        if private_data:
            with open(PRIVATE_FILE, "w", encoding="utf-8") as f:
                f.write("\n".join(private_data) + f"\n\n# Sync: {sync_time}")
        print(f"Emergency update triggered: {active_port}")
    except Exception as e:
        print(f"Update failed: {e}")

if __name__ == "__main__":
    # 如果仓库状态异常，或者你手动想跑，就执行对时更新
    if not check_repo_health():
        print("Health check failed, starting emergency scan...")
        do_update()
    else:
        print("All repos are healthy and up-to-date.")
