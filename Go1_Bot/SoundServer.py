import os
import socket


def play():
    os.system("aplay -D plughw:2,0 cat.wav")


if __name__ == "__main__":
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.bind(("192.168.123.13", 8888))
    print("UDP bound on port 8888...")

    # 设置音量为50%
    os.system("amixer -c 2 set Speaker 18")
    # 终止其他占用扬声器的进程
    os.system("ps -aux | grep wsaudio | awk '{print $2}' | xargs kill -9")

    while True:
        print("Waiting for client...")
        data, addr = s.recvfrom(1024)
        print("Receive from %s:%s" % addr)
        if data == b"play":
            play()