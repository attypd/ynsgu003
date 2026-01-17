import requests
import time

TARGETS = {"凤凰中文": "68a6abe2000dd5d9a5012600500a1279"}
HOST = "focus169.org"
# 只测你最确定的这三个，节约时间
CHECK_PORTS = [48719, 48720, 8080]

def diagnostic_check(port):
    token = TARGETS["凤凰中文"]
    url = f"http://{HOST}:{port}/{token}"
    # 增加更真实的浏览器头
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) PotPlayer/1.7",
        "Connection": "keep-alive"
    }
    
    print(f"\n🔍 诊断开始 -> 端口: {port}")
    try:
        start_t = time.time()
        # 将超时增加到 100 秒，确保盖过 48 秒的延迟
        with requests.get(url, headers=headers, stream=True, timeout=100) as r:
            print(f"📡 收到响应！状态码: {r.status_code}")
            if r.status_code == 200:
                print("⏳ 状态 200 OK，正在等待视频流数据 (预计需 48s+)...")
                # 尝试读取前 1024 字节
                for chunk in r.iter_content(chunk_size=1024):
                    if chunk:
                        print(f"✅ 【大功告成】耗时 {time.time()-start_t:.1f}s 抓取到真实流数据！")
                        return True
            else:
                print(f"⚠️ 服务器拒绝了请求，可能需要更换 Token 或 IP 被封。")
    except Exception as e:
        print(f"❌ 错误详情: {e}")
    return False

if __name__ == "__main__":
    found_any = False
    for p in CHECK_PORTS:
        if diagnostic_check(p):
            with open("active_port.txt", "w", encoding="utf-8") as f:
                f.write(f"凤凰中文,http://{HOST}:{p}/{TARGETS['凤凰中文']}")
            found_any = True
            break
    
    if not found_any:
        print("\n实验结论：所有端口均未能在 100 秒内吐出数据。")
