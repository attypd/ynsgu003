import socket
import time

# --- P3P 专攻配置 ---
HOST = "focus169.org"
PORT = 48719
TOKEN = "68a6abe2000dd5d9a5012600500a1279"

def p3p_raw_probe():
    print(f"📡 启动 P3P 协议原始套接字探测: {HOST}:{PORT}")
    
    # 构造一个符合 P3P/P2P 壳子特征的原始二进制请求
    # 这种源不需要完整的 HTTP 报文，它们更看重底层的 Keep-Alive 活性
    raw_request = (
        f"GET /{TOKEN} HTTP/1.1\r\n"
        f"Host: {HOST}:{PORT}\r\n"
        "User-Agent: okhttp/3.12.13\r\n"
        "Accept: */*\r\n"
        "Connection: Keep-Alive\r\n"
        "P3P: CP='CURa ADMa DEVa PSAo PSDo OUR BUS UNI PUR INT DEM STA PRE COM NAV OTC NOI DSP COR'\r\n\r\n"
    ).encode('utf-8')

    start_t = time.time()
    try:
        # 1. 建立原始 TCP 连接
        sock = socket.create_connection((HOST, PORT), timeout=10)
        print("🔗 TCP 物理层已连通，开始注入 P3P 握手信号...")
        
        sock.sendall(raw_request)
        
        # 2. 针对 48 秒延迟，我们进入“静默监听”模式
        # P3P 源在准备好数据前不会回任何东西，我们只看连接是否被强踢
        sock.settimeout(100) 
        
        # 尝试读取前 1 字节（只要能读到，说明协议握手成功）
        data = sock.recv(1)
        
        if data:
            print(f"✅ 【P3P 撞击成功】耗时 {time.time()-start_t:.1f}s 捕获到协议数据包！")
            with open("active_port.txt", "w") as f:
                f.write(f"凤凰中文,http://{HOST}:{PORT}/{TOKEN}")
            return
            
    except socket.timeout:
        # 如果超时但没被拒绝，对 P3P 源来说大概率也是活的
        print("⚠️ 握手超时但连接未断开，该端口具备 P3P 典型挂起特征。")
        with open("active_port.txt", "w") as f:
            f.write(f"凤凰中文(待测),http://{HOST}:{PORT}/{TOKEN}")
    except Exception as e:
        msg = f"❌ P3P 探测崩溃: {str(e)}"
        print(msg)
        with open("active_port.txt", "w") as f:
            f.write(msg)
    finally:
        if 'sock' in locals(): sock.close()

if __name__ == "__main__":
    p3p_raw_probe()
