import socket
import time
from concurrent.futures import ThreadPoolExecutor

# --- 核心配置 ---
HOST = "focus169.org"
# 锁定你提供的 48719，并顺带扫一下周边可能的开口
SCAN_PORTS = [48719, 48718, 48720, 8080, 80, 48710]
# 你的有效 Token 库
TOKENS = {
    "凤凰中文": "68a6abe2000dd5d9a5012600500a1279",
    "凤凰资讯": "694531d0000414f210386f2756d64099",
    "凤凰香港台": "68a6b0e900041c3da514c6d1105e4d0d",
    "翡翠台": "694533620009fd15103e92fc6c853ea8"
}

def quick_check(port):
    """只做物理连接，不发任何数据包，防屏蔽"""
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(1.5) # 1.5秒不给反应直接断开，绝不墨迹
        if s.connect_ex((HOST, port)) == 0:
            return port
        s.close()
    except:
        pass
    return None

if __name__ == "__main__":
    print(f"🚀 启动 P3P 并发秒扫任务...")
    start_t = time.time()
    
    # 瞬间并发敲门
    with ThreadPoolExecutor(max_workers=10) as executor:
        active_ports = list(filter(None, executor.map(quick_check, SCAN_PORTS)))
    
    if active_ports:
        print(f"🔥 发现有效开口: {active_ports}")
        results = []
        for p in active_ports:
            for name, token in TOKENS.items():
                # 严格按照你截图中要求的 p3p:// 格式输出
                results.append(f"{name},p3p://{HOST}:{p}/{token}")
        
        with open("active_port.txt", "w", encoding="utf-8") as f:
            f.write("\n".join(results))
        print(f"✅ 更新成功，总耗时 {time.time()-start_t:.1f}s")
    else:
        # 如果全挂，也要更新文件，让你知道扫描跑过了
        with open("active_port.txt", "w", encoding="utf-8") as f:
            f.write(f"❌ 扫描完毕时间 {time.strftime('%H:%M:%S')}，端口全线封锁。")
