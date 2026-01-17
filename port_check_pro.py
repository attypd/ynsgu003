import requests
import time

# 只锁定你最确定的端口，不浪费时间
HOST = "focus169.org"
TOKEN = "68a6abe2000dd5d9a5012600500a1279"
PORT = 48719 

def fast_probe():
    url = f"http://{HOST}:{PORT}/{TOKEN}"
    # 强化 User-Agent，完全模拟 PotPlayer 的 P2P 开启模式
    headers = {
        "User-Agent": "PotPlayer/1.7 (Windows NT 10.0; Win64; x64; p3p/1.0)",
        "Accept": "*/*",
        "Icy-MetaData": "1",
        "Connection": "Keep-Alive"
    }
    
    start_time = time.time()
    result_msg = ""

    print(f"🚀 启动极速探测 (限时 100s)... 目标: {PORT}")
    try:
        # 增加 headers 探测，不强制读取流内容以兼容 P3P
        r = requests.get(url, headers=headers, stream=True, timeout=80)
        
        status = r.status_code
        result_msg = f"Time: {time.time()-start_t:.1f}s, Status: {status}"
        
        if status == 200:
            # 只要状态码对，直接判定成功并写入
            with open("active_port.txt", "w") as f:
                f.write(f"凤凰中文,http://{HOST}:{PORT}/{TOKEN}")
            print(f"✅ 成功！状态 200，耗时 {time.time()-start_time:.1f}s")
            return
        else:
            result_msg += f" | Error: Server returned {status}"
    except Exception as e:
        result_msg = f"❌ 失败原因: {str(e)}"

    # 失败也写个日志，让你知道哪里断了
    with open("active_port.txt", "w") as f:
        f.write(result_msg)
    print(result_msg)

if __name__ == "__main__":
    fast_probe()
