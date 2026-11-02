import os

# 从前面日志中固定的会员鉴权参数
AUTH_PARAMS = (
    "&userid="
    "&mac=96:C9:BB:C8:5F:33"
    "&playkey=7b874064e67db98b11646fd0f35f1b85"
    "&username=1183534995"
    "&key=52ea2cdbb710a4cfa792bb5f212085bd"
)

def main():
    input_file = "focus_raw.txt"   # 你的原始 p3p 源文件
    output_file = "total_live.txt" # 仓库里现成的输出目标文件（可直接对接OK影视）

    if not os.path.exists(input_file):
        print(f"未找到原始文件: {input_file}")
        return

    with open(input_file, "r", encoding="utf-8") as f:
        lines = f.readlines()

    new_lines = []

    for line in lines:
        line = line.strip()
        if not line:
            continue

        # 保留分类标签行（如 焦点香港,#genre#）
        if "#genre#" in line:
            new_lines.append(line)
            continue

        # 解析 p3p 格式并转换为本地 9906 代理链接
        if ",p3p://" in line:
            name, url_part = line.split(",p3p://", 1)

            if "&id/" in url_part:
                server, chan_id = url_part.split("&id/", 1)
            elif "&id=" in url_part:
                server, chan_id = url_part.split("&id=", 1)
            else:
                new_lines.append(line)
                continue

            # 拼接标准代理播放地址
            http_url = (
                f"http://127.0.0.1:9906/cmd.xml?cmd=switch_chan"
                f"&server={server}&id={chan_id}{AUTH_PARAMS}"
            )
            new_lines.append(f"{name},{http_url}")
        else:
            new_lines.append(line)

    # 写入目标文件
    with open(output_file, "w", encoding="utf-8") as f:
        f.write("\n".join(new_lines))

    print("p3p源转换并同步到 total_live.txt 成功！")

if __name__ == "__main__":
    main()
