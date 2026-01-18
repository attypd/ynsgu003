import requests
import concurrent.futures
import time
import re
from datetime import datetime, timedelta

# 配置
DOMAIN = "url.cdnhs.store"

def check_port(port):
    """探测端口：识别 200 和 302 重定向"""
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
    is_private_section = False # 标记是否已经进入私密分组
    
    try:
        # 读取你原始上传的源文件
        with open("cvs_mylive.txt", "r", encoding="utf-8") as f:
            lines = f.readlines()
            
        for line in lines:
            line = line.strip()
            if not line: continue
            
            # 1. 精准替换端口
            updated_line = re.sub(r':\d+/', f':{new_port}/', line)
            total_lines.append(updated_line)
            
            # 2. 核心逻辑：精准匹配私密频道分组标题
            # 只要这一行包含“私密频道”和“#genre#”，后面所有的行都会被存入独立文件
            if "私密频道" in updated_line and "#genre#" in updated_line:
                is_private_section = True
            
            if is_private_section:
                private_only_lines.append(updated_line)
                
    except Exception as e:
        print(f"读取失败: {e}")
        return

    # 生成 1: 完整版 (顺序完全不动)
    with open("total_live.txt", "w", encoding="utf-8") as f:
        f.write("\n".join(total_lines))
        f.write(f"\n\n# 自动对时更新: {bj_time} | 端口: {new_port}")

    # 生成 2: 独立版 (只包含私密频道分组)
    if private_only_lines:
        with open("private_only.txt", "w", encoding="utf-8") as f:
            f.write("\n".join(private_only_lines))
    else:
        print("警告：未在源文件中找到 '私密频道' 分组标记")

    print(f"✅ 更新成功！发现端口: {new_port} | 北京时间: {bj_time}")

if __name__ == "__main__":
    update_files()
