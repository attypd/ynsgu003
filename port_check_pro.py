import requests
import time

# 配置
HOST = "focus169.org"
TOKEN = "68a6abe2000dd5d9a5012600500a1279"
PORTS = [48719, 48720, 8080]

def check():
    results = []
    results.append(f"⏰ 开始任务时间: {time.strftime('%Y-%m-%d %H:%M:%S')}")
    
    for port in PORTS:
        url = f"http://{HOST}:{port}/{TOKEN}"
        results.append(f"\n🔍 正在测试端口: {port}")
        try:
            # 针对你说的48秒延迟，这里给 100 秒
            with requests.get(url, timeout=100, stream=True) as r:
                results.append(f"➡️ 状态码: {r.status_code}")
                if r.status_code == 200:
                    results.append("⏳ 状态 OK，等待数据流...")
                    # 尝试读一点数据
                    for chunk in r.iter_content(chunk_size=1024):
                        if chunk:
                            results.append("✅ 成功抓到视频流！")
                            break
        except Exception as e:
            results.append(f"❌ 错误原因: {str(e)}")
            
    # 无论如何都生成这个文件！
    with open("active_port.txt", "w", encoding="utf-8") as f:
        f.write("\n".join(results))
    print("📢 报告已强制写入 active_port.txt")

if __name__ == "__main__":
    check()
