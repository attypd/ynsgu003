import requests
import concurrent.futures
import time
import re

# 配置
DOMAIN = "url.cdnhs.store"
# 识别私密频道的关键词（用于置后和单独分组）
PRIVATE_KEYWORDS = [
    "松视", "sonsee", "彩虹", "Rainbow", "潘多拉", "Pandora", "惊艳", "Amazing", 
    "香蕉", "Banana", "happy", "HappyHD", "极限", "JStar", "花花公子", "Playboy", 
    "日本", "Pigoo", "Extasy", "Private", "Red Light", "CineMan", "Dorcel", "FapTV"
]

def check_port(port):
    """探测端口：识别 200 和 302 重定向"""
    test_url = f"http://{DOMAIN}:{port}/mytv.php?id=3"
    try:
        # allow_redirects=False 关键：不跟随重定向，直接捕捉 302 状态
        res = requests.head(test_url, timeout=1.5, allow_redirects=False)
        if res.status_code in [200, 302]:
            return str(port)
    except:
        return None
    return None

def get_latest_port():
    """全自动扫描 40000-50000 端口"""
    for p in [48559, 48867, 8080]: # 优先检查常用活跃点
        if check_port(p): return str(p)
    
    with concurrent.futures.ThreadPoolExecutor(max_workers=100) as executor:
        ports = range(40000, 50000)
        results = executor.map(check_port, ports)
        for r in results:
            if r: return r
    return "48559"

def update_files():
    new_port = get_latest_port()
    bj_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time() + 8*3600))
    
    normal_part = []
    private_part = ["私密频道,#genre#"]
    
    try:
        with open("cvs_mylive.txt", "r", encoding="utf-8") as f:
            lines = f.readlines()
            
        for line in lines:
            line = line.strip()
            if not line or "MYlive" in line: continue
            
            # 正则替换：匹配 http://域名:端口/ 中的端口部分
            updated_line = re.sub(r':\d+/', f':{new_port}/', line)
            
            # 逻辑判定：是否属于私密频道
            if any(k.lower() in updated_line.lower() for k in PRIVATE_KEYWORDS):
                if ",#genre#" not in updated_line:
                    private_part.append(updated_line)
            else:
                normal_part.append(updated_line)
                
    except Exception as e:
        print(f"读取源文件失败: {e}")
        return

    # 生成 1：全套源 (total_live.txt) - 私密频道在最后
    with open("total_live.txt", "w", encoding="utf-8") as f:
        f.write("\n".join(normal_part))
        f.write("\n\n") # 空行分隔
        f.write("\n".join(private_part))
        f.write(f"\n\n# 自动更新: {bj_time} | 端口: {new_port}")

    # 生成 2：单独私密频道 (private_only.txt)
    with open("private_only.txt", "w", encoding="utf-8") as f:
        f.write("\n".join(private_part))

    print(f"✅ 更新成功！发现活跃端口: {new_port}")

if __name__ == "__main__":
    update_files()
