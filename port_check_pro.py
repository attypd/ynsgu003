import requests
import time

# --- 目标配置 ---
TARGETS = {"凤凰中文": "68a6abe2000dd5d9a5012600500a1279"}
HOST = "focus169.org"
# 重点测试你提供的有效端口
CHECK_PORTS = [48719, 48718, 48720, 8080]

def deep_check(port):
    token = TARGETS["凤凰中文"]
    url = f"http://{HOST}:{port}/{token}"
    headers = {"User-Agent": "PotPlayer/1.7"}
    
    print(f"📡 正在深度探测端口 {port}...")
    print(f"⏳ 预警：该源出图极慢，脚本将模拟播放器死等 80 秒，请勿手动取消...")
    
    try:
        start_time = time.time()
        # 【关键】：stream=True 保持长连接握手，timeout=90 给足预热时间
        with requests.get(url, headers=headers, stream=True, timeout=90) as r:
            if r.status_code == 200:
                # 模拟播放器读取流数据，只要读到 1 字节就说明有效
                for chunk in r.iter_content(chunk_size=1024):
                    if chunk:
                        elapsed = time.time() - start_time
                        print(f"✅ 探测成功！耗时 {elapsed:.1f} 秒抓取到视频流。")
                        return True
    except Exception as e:
        print(f"❌ 端口 {port} 探测结束：在规定时间内未收到有效数据。")
    return False

if __name__ == "__main__":
    print(f"🚀 开始对 {HOST} 进行业务端口存活验证...")
    found = False
    for p in CHECK_PORTS:
        if deep_check(p):
            # 结果存盘，供 Actions 自动提交
            with open("active_port.txt", "w", encoding="utf-8") as f:
                f.write(f"凤凰中文,http://{HOST}:{p}/{TARGETS['凤凰中文']}")
            found = True
            break
    
    if found:
        print("\n🎯 任务成功：有效源已记录至 active_port.txt")
    else:
        print("\n❌ 任务结束：未发现可用端口。")
