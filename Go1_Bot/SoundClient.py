import time
import socket 


def play(ip, port):
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    addr = (ip, port)
    s.sendto("play".encode(), addr)
    time.sleep(1)
    s.close()


if __name__ == "__main__":
    play("192.168.123.13", 8888)