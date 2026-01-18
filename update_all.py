import requests
import concurrent.futures
import time
import re
from datetime import datetime, timedelta

# 配置
DOMAIN = "url.cdnhs.store"

def check_port(port):
    """探测端口：支持 200 和 302 重定向"""
    test_url = f"http://{DOMAIN}:{port}/mytv.php?id=3"
    try:
        res = requests.head(test_url, timeout=1.5, allow_redirects=False)
        if res.status_code in [200, 302]:
            return str(port)
    except:
        return None
    return None

def get_latest_port():
    """全自动扫描端口"""
    for p in [48867, 48559, 8080]:
        if check_port(p): return str(p)
    with concurrent.futures.ThreadPoolExecutor(max_workers=100) as executor:
        ports = range(40000, 50000)
        results = executor.map(check_port, ports)
        for r in results:
            if r: return r
    return "48559"

def update_files():
    new_port = get_latest_port()
    bj_time = (datetime.utcnow() + timedelta(hours=8)).strftime('%Y-%m-%d %H:%M:%S')
    
    total_lines = []
    private_only_lines = []
    is_private_section = False # 标记是否进入了私密分组
    
    try:
        with open("cvs_mylive.txt", "r", encoding="utf-8") as f:
            lines = f.readlines()
            
        for line in lines:
            line = line.strip()
            if not line: continue
            
            # 1. 替换端口 (只做这一件事，不改位置)
            updated_line = re.sub(r':\d+/', f':{new_port}/', line)
            total_lines.append(updated_line)
            
            # 2. 识别并提取私密频道部分 (用于单独生成文件)
            # 假设你文件里私密分组的标题包含 "私密频道" 四个字
            if "私密频道,#genre#" in updated_line:
                is_private_section = True
            
            if is_private_section:
                private_only_lines.append(updated_line)
                
    except Exception as e:
        print(f"读取失败: {e}")
        return

    # 生成 1: total_live.txt (顺序跟你的 cvs_mylive.txt 完全一样，只是端口变了)
    with open("total_live.txt", "w", encoding="utf-8") as f:
        f.write("\n".join(total_lines))
        f.write(f"\n\n# 自动对时更新: {bj_time} | 端口: {new_port}")

    # 生成 2: private_only.txt (只包含私密频道那一组的内容)
    with open("private_only.txt", "w", encoding="utf-8") as f:
        f.write("\n".join(private_only_lines))

    print(f"✅ 更新成功！端口: {new_port} | 时间: {bj_time}")

if __name__ == "__main__":
    update_files()
