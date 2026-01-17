import socket, concurrent.futures, sys

# 域名防爬
H = "focus" + "169" + ".org"
# 降低到 60 线程更稳，不容易被屏蔽；超时增加到 2 秒确保抓到响应
W = 60 
R = range(10000, 60001)

S = [
    ["焦点香港", "凤凰资讯", "这里填后缀"],
    ["焦点香港", "翡翠台", "这里填后缀"],
    ["焦点电影", "CCM 天映经典", "64124d990007b0aaa0d9131033d9354a"],
    ["焦点电影", "CCM 天映经典 CN中英字幕", "64124dd500082194a0d9fd8d736a3dff"],
]

def check(p):
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.settimeout(2.0) # 增加到 2 秒，大幅提高扫描成功率
            if s.connect_ex((H, p)) == 0:
                return p
    except: pass
    return None

def main():
    print(f"正在深度扫描 {H}...")
    p_found = None
    with concurrent.futures.ThreadPoolExecutor(max_workers=W) as ex:
        # 将端口打乱顺序扫描，更容易绕过简单防护
        import random
        ports = list(R)
        random.shuffle(ports)
        
        futs = {ex.submit(check, p): p for p in ports}
        for f in concurrent.futures.as_completed(futs):
            res = f.result()
            if res:
                p_found = res
                ex.shutdown(wait=False, cancel_futures=True)
                break
    
    if p_found:
        out = [f"{g},#genre#\n{n},p3p://{H}:{p_found}/{s}" for g,n,s in S]
        with open("config_v2.txt", "w", encoding="utf-8") as f:
            f.write("\n".join(out))
        print(f"成功抓取到有效端口: {p_found}")
    else:
        print("本次未发现有效端口，建议半小时后自动重试。")
        sys.exit(1)

if __name__ == "__main__": main()
