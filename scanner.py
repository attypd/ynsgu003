import socket, concurrent.futures, sys

# 域名防爬处理
D = "focus" + "169" + ".org"
W = 100 
R = range(10000, 60001)

# 频道列表 (分类, 名称, 后缀)
# 请务必在此处填入你抓到的真实后缀
S = [
    ["焦点香港", "凤凰资讯", "这里填后缀"],
    ["焦点香港", "凤凰香港台", "这里填后缀"],
    ["焦点香港", "翡翠台", "这里填后缀"],
    ["焦点电影", "CCM 天映经典", "64124d990007b0aaa0d9131033d9354a"],
    ["焦点电影", "CCM 天映经典 CN中英字幕", "64124dd500082194a0d9fd8d736a3dff"],
]

def c(p):
    """快速探测端口"""
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.settimeout(1.0) # 1秒超时，保证扫描效率
            return p if s.connect_ex((D, p)) == 0 else None
    except: return None

def main():
    print("正在捕捉最新有效端口...")
    p_now = None
    # 100线程并发扫描 5万个端口
    with concurrent.futures.ThreadPoolExecutor(W) as ex:
        futs = {ex.submit(c, p): p for p in R}
        for f in concurrent.futures.as_completed(futs):
            res = f.result()
            if res:
                p_now = res
                # 一旦捕捉到新端口，立刻中断其他扫描任务，抢时间更新
                ex.shutdown(wait=False, cancel_futures=True)
                break
    
    if p_now:
        out = []
        cur_g = ""
        for g, n, suf in S:
            if g != cur_g:
                out.append(f"{g},#genre#")
                cur_g = g
            # 使用 p3p 协议拼接最新端口
            out.append(f"{n},p3p://{D}:{p_now}/{suf}")
        
        # 写入隐蔽文件 config_v2.txt
        with open("config_v2.txt", "w", encoding="utf-8") as f:
            f.write("\n".join(out))
        print(f"更新成功! 最新端口: {p_now}")
    else:
        print("未发现有效端口，请检查网络或目标服务器状态")
        sys.exit(1)

if __name__ == "__main__": main()
