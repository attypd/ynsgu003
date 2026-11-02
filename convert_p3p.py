import os

def main():
    input_file = "focus_raw.txt"   # 原始源文件（你只需要维护这里面的 p3p 源）
    output_file = "total_live.txt" # 自动化生成的最终文件（给 OK 影视使用）

    # 检查原始文件是否存在
    if not os.path.exists(input_file):
        print(f"错误：未找到原始文件 {input_file}，请先创建它并放入 p3p 源内容！")
        return

    with open(input_file, "r", encoding="utf-8") as f:
        lines = f.readlines()

    new_lines = []
    for line in lines:
        line = line.strip()
        if not line:
            continue

        # 保留分类标题行（如 焦点香港,#genre#）
        if "#genre#" in line:
            new_lines.append(line)
            continue

        # 将 p3p:// 转换为本地 9906 直连代理格式
        if "p3p://" in line and "127.0.0.1" not in line:
            new_line = line.replace("p3p://", "http://127.0.0.1:9906/")
            new_lines.append(new_line)
        else:
            new_lines.append(line)

    # 每次都全新生成/覆盖 total_live.txt
    with open(output_file, "w", encoding="utf-8") as f:
        f.write("\n".join(new_lines))

    print(f"成功：已从 {input_file} 重新生成并覆盖 {output_file}！")

if __name__ == "__main__":
    main()
