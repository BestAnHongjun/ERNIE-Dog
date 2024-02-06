# 3.2 如何调用狗子的扬声器

阅读本教程之前请先阅读[官方教程](https://www.yuque.com/ironfatty/nly1un/avam9z)，了解相关基础知识。

调用狗子扬声器的思路跟调用灯带的思路很像，都是通过`python`的`os.system()`函数直接执行相关指令，控制扬声器播放特定的wav文件。

比如，在本项目中，为大家准备了一个wav文件，位于`Go1_Bot/cat.wav`，没错！你没有听错！这是小汪独特的叫声！

然后，我们可以进入Go1-Nano1板卡，编写如下python脚本并执行：

```py
import os

# 设置音量为50%
os.system("amixer -c 2 set Speaker 18")
# 终止其他占用扬声器的进程
os.system("ps -aux | grep wsaudio | awk '{print $2}' | xargs kill -9")
# 播放wav文件
os.system("aplay -D plughw:2,0 cat.wav")
```

但是我们遇到一个问题，扬声器是连接在Nano1板卡上的，所以我们只能在Nano1板卡上通过调用`os.system()`去播放音频。但是我们的主控程序是运行在NX板卡上的，如何在NX上控制Nano1播放音频呢？

看来我们需要自己手写一个UDP通信程序了[手动狗头]，关于UDP通信的具体原理不是本baseline教授的内容，请自行学习《计算机网络》这门课。本baseline仅教授如何使用。

首先我们编写一个`SoundServer.py`程序，运行在Nano1板卡上：

```py
import os
import socket


# 调用该函数，就播放wav音频
def play():
    os.system("aplay -D plughw:2,0 cat.wav")


if __name__ == "__main__":
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    # 绑定socket的ip与端口，ip地址不要修改，123.13就是nano1的本地ip；8888端口号可任意修改，只要不与其他服务冲突即可
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

        # 如果UDP接收到的内容是“play”，就调用函数播放音频
        if data == b"play":
            play()

```

至此，一个非常简单的音频服务程序就写好了，在Nano1上运行：

```sh
cd Go1_bot
python SoundServer.py
```

服务端写好了，我们还需要再NX上写一个客户端程序`SoundClient.py`，如下：

```py
import time
import socket 


def play(ip, port):
    # 初始化socket
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    # 设置目标ip和端口号
    addr = (ip, port)
    # 向服务端发送“play”
    s.sendto("play".encode(), addr)
    # 灯带1s
    time.sleep(1)
    # 关闭socket
    s.close()


if __name__ == "__main__":
    # 端口号要与服务端对应！！！
    play("192.168.123.13", 8888)
```

一个十分简易的客户端也写好了，是不是非常简单！

在NX板卡上运行该程序：

```sh
cd Go1_Bot
python SoundClient.py
```

然后咱们的小汪就开始叫了！
