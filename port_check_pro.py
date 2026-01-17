import http.client
import time
import socket

# --- 目标配置 ---
HOST = "focus169.org"
PORT = 48719
URI = "/68a6abe2000dd5d9a5012600500a1279"

def simulate_ok_player():
    print(f"🎬 正在模拟 OK影视 壳子内核连接 {HOST}:{PORT}...")
    
    # 模仿 OK 壳子常见的 User-Agent 和 Icy 头部
    headers = {
        "User-Agent": "okhttp/3.12.13", # OK 壳子最常用的底层网络库
        "Accept": "*/*",
        "Icy-MetaData": "1",
        "Connection": "Keep-Alive",
        "Accept-Encoding": "gzip",
        "Host": f"{HOST}:{PORT}"
    }

    try:
        start_t = time.time()
        # 使用底层的 http.client 避开 requests 的握手特征
        conn = http.client.HTTPConnection(HOST, PORT, timeout=100)
        
        # 发起请求
        conn.request("GET", URI, headers=headers)
        
        # 等待响应
        response = conn.getresponse()
        print(f"📡 壳子握手成功！状态码: {response.status}")
        
        if response.status == 200:
            print("⏳ 状态码正确，进入深度缓冲等待 (48s+)...")
            # 模仿壳子读取数据流
            # 只要能在 90 秒内读到第一个字节，就说明端口是活的
            data = response.read(1024) 
            if data:
                elapsed = time.time() - start_t
                success_msg = f"✅ OK 壳子模拟成功！耗时 {elapsed:.1f}s 抓取到视频流。"
                print(success_msg)
                with open("active_port.txt", "w", encoding="utf-8") as f:
                    f.write(f"凤凰中文,http://{HOST}:{PORT}{URI}")
                return
    except Exception as e:
        error_msg = f"❌ 壳子连接失败: {str(e)}"
        print(error_msg)
        with open("active_port.txt", "w", encoding="utf-8") as f:
            f.write(error_msg)

if __name__ == "__main__":
    simulate_ok_player()
