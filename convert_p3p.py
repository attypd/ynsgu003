import os

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

        # 直接将 p3p:// 替换为本地 9906 代理直连地址
        if "p3p://" in line:
            # 例如：星空卫视,p3p://focus169.org:35351&id/...
            # 转换后：星空卫视,http://127.0.0.1:9906/focus169.org:35351&id/...
            new_line = line.replace("p3p://", "http://127.0.0.1:9906/")
            new_lines.append(new_line)
        else:
            # 非 p3p 格式原样保留
            new_lines.append(line)

    # 原地写回 total_live.txt
    with open(target_file, "w", encoding="utf-8") as f:
        f.write("\n".join(new_lines))

    print("成功：已将 p3p 转换为本地 9906 直连代理格式！")

if __name__ == "__main__":
    main()
