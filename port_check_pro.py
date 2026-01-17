import socket
from concurrent.futures import ThreadPoolExecutor
import time

# --- 核心配置 ---
HOST = "focus169.org"
# 这里的 Token 只要有一个活的，整个端口就是通的
TOKEN_SAMPLES = {
    "凤凰中文": "68a6abe2000dd5d9a5012600500a1279",
    "凤凰资讯": "694531d0000414f210386f2756d64099"
}
# 重点扫 48719 周边的开口
SCAN_PORTS = [48719, 48718, 48720, 8080, 80, 8000]

def p3p_knock(port):
    """
    像壳子一样快速敲门，不纠结 P3P 握手数据，只看端口是否存活
    """
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(2) # 2秒不通直接滚，这就是效率
        result = s.connect_ex((HOST, port))
        if result == 0:
            return port
        s.close()
    except:
        pass
    return None

if __name__ == "__main__":
    print(f"📡 正在以 P3P 并发模式探测 {HOST}...")
    start_time = time.time()
    
    # 使用 10 个线程并发，瞬间扫完所有备选端口
    with ThreadPoolExecutor(max_workers=10) as executor:
        active_ports = list(filter(None, executor.map(p3p_knock, SCAN_PORTS)))
    
    if active_ports:
        print(f"🔥 捕获到有效开口: {active_ports}")
        with open("active_port.txt", "w", encoding="utf-8") as f:
            for p in active_ports:
                for name, token in TOKEN_SAMPLES.items():
                    # 按照你截图中显示的 p3p 格式输出
                    f.write(f"{name},p3p://{HOST}:{p}/{token}\n")
        print(f"✅ 探测成功，总耗时: {time.time()-start_time:.1f}秒")
    else:
        print("❌ 核心端口全军覆没，可能 IP 被封锁。")
