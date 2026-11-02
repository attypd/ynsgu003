import os

# 定义从日志中提取的标准鉴权参数（严格使用 & 拼接，不使用 $）
AUTH_QUERY = (
    "&userid="
    "&mac=96:C9:BB:C8:5F:33"
    "&playkey=7b874064e67db98b11646fd0f35f1b85"
    "&username=1183534995"
    "&key=52ea2cdbb710a4cfa792bb5f212085bd"
)

def main():
    target_file = "total_live.txt"  # 操作目标文件
    
    if not os.path.exists(target_file):
        print(f"错误：未找到文件 {target_file}")
        return

    with open(target_file, "r", encoding="utf-8") as f:
        lines = f.readlines()

    new_lines = []
    for line in lines:
        line = line.strip()
        if not line:
            continue

        # 保留分类标题行（如 🇨🇳焦点香港,#genre#）
        if "#genre#" in line:
            new_lines.append(line)
            continue

        # 解析 p3p 协议链接
        if ",p3p://" in line:
            name, url_part = line.split(",p3p://", 1)

            # 兼容不同的 id 分隔符（&id/ 或 &id=）
            if "&id/" in url_part:
                server, chan_id = url_part.split("&id/", 1)
            elif "&id=" in url_part:
                server, chan_id = url_part.split("&id=", 1)
            else:
                new_lines.append(line)
                continue

            # 严格按照标准格式拼接：cmd.xml?cmd=switch_chan&server=xxx&id=xxx&userid=&mac=...
            http_url = (
                f"http://127.0.0.1:9906/cmd.xml?cmd=switch_chan"
                f"&server={server}&id={chan_id}{AUTH_QUERY}"
            )
            new_lines.append(f"{name},{http_url}")
        else:
            # 非 p3p 格式原样保留
            new_lines.append(line)

    # 原地写回 total_live.txt
    with open(target_file, "w", encoding="utf-8") as f:
        f.write("\n".join(new_lines))

    print("成功：total_live.txt 链接格式已修正！")

if __name__ == "__main__":
    main()
