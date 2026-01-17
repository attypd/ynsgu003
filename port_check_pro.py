import socket
import time

# --- 配置：只写你截图中成功的 HOST 和已知端口 ---
HOST = "focus169.org"
# 别人能扫出来，说明 48719 肯定是活的
CHECK_PORTS = [48719, 48718, 48720, 8080, 8000]
TOKENS = {
    "凤凰中文": "68a6abe2000dd5d9a5012600500a1279",
    "凤凰资讯": "694531d0000414f210386f2756d64099",
    "凤凰香港台": "68a6b0e900041c3da514c6d1105e4d0d"
}

def quick_knock():
    found_any = False
    results = []
    
    for port in CHECK_PORTS:
        print(f"📡 正在物理撞击端口: {port}...")
        try:
            # 极速探测：2秒连不上就撤
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.settimeout(2)
            if s.connect_ex((HOST, port)) == 0:
                print(f"🔥 捕获到活动端口: {port}")
                for name, token in TOKENS.items():
                    # 严格按照你给的截图格式输出
                    results.append(f"{name},p3p://{HOST}:{port}/{token}")
                found_any = True
            s.close()
        except:
            continue

    if found_any:
        with open("active_port.txt", "w", encoding="utf-8") as f:
            f.write("\n".join(results))
        print("✅ 更新成功：最新 P3P 地址已存入 active_port.txt")
    else:
        # 如果全失败，强制生成错误日志，证明脚本确实跑了
        with open("active_port.txt", "w", encoding="utf-8") as f:
            f.write(f"❌ 扫描结束时间 {time.ctime()}，未发现开放端口。")

if __name__ == "__main__":
    quick_knock()
