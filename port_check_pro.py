import requests
import time

# --- 配置 ---
TARGETS = {
    "凤凰中文": "68a6abe2000dd5d9a5012600500a1279",
}
HOST = "focus169.org"
# 既然 48719 是有效端口，我们重点测它以及周围的几个偏移量
CHECK_PORTS = [48719, 48718, 48720, 8080, 80]

def deep_check(port):
    token = TARGETS["凤凰中文"]
    url = f"http://{HOST}:{port}/{token}"
    headers = {
        "User-Agent": "PotPlayer/1.7",
        "Range": "bytes=0-1024" # 模拟播放器请求前 1KB 数据
    }
    
    print(f"正在深度探测端口 {port}，由于源响应慢，请耐心等待 60 秒...")
    try:
        # 【关键】：timeout 设置为 70 秒，给服务器足够的响应时间
        start_time = time.time()
        with requests.get(url, headers=headers, stream=True, timeout=70) as r:
            if r.status_code == 200:
                # 尝试读取第一块数据
                for chunk in r.iter_content(chunk_size=512):
                    if chunk:
                        duration = time.time() - start_time
                        print(f"✅ 成功！端口 {port} 在 {duration:.1f} 秒后成功返回视频流！")
                        return True
    except Exception as e:
        print(f"❌ 端口 {port} 验证失败: {e}")
    return False

def main():
    for port in CHECK_PORTS:
        if deep_check(port):
            print(f"找到真正活着的源：http://{HOST}:{port}/{TARGETS['凤凰中文']}")
            break

if __name__ == "__main__":
    main()
