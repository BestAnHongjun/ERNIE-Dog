# 3.1 如何让狗子的灯带发光

阅读本教程之前请先阅读[官方教程](https://www.yuque.com/ironfatty/nly1un/cmls8h)，了解相关基础知识。

Go1头部灯带的官方开发SDK位于狗子Nano1板卡的`~/Unitree/SDK`目录下，本Baseline对其进行整理后放在了`Go1_Bot/FaceLightSDK`目录下，主要对`main.cpp`做了相关修改。

该SDK的基本原理是，通过配置一个struct结构体，基于UDP协议发送给运行在Nano1板卡上的灯带控制服务。具体的协议内容宇树并没有开源，而是封装在了一个链接库里面，而且只提供了`C++`版本的例程。本Baseline本着能简就简的原则，思路是：

* 编写一个固定的控制带灯闪烁的程序，编译成二进制文件，在`python`程序中使用`os.system()`函数进行调用。

对于各路大佬，也可自行尝试以下工程集成思路：
* 整个工程干脆全用C++开发（追求运行效率的首选方案）
* 自己写一个python的C++扩展接口，让python直接调用二进制库
* 用抓包程序看一下UDP协议包，然后用`python socket`复现该协议（有点 ni xiang gong cheng了，复现了协议自己留着用就行，别到网上宣扬，协议版权归宇树所有）

OK，下面进入正题。

我们进入Go1-NX板卡，编写新的`main.cpp`：

```cpp
#include "FaceLightClient.h"

int main(){
    FaceLightClient client;

    client.setAllLed(client.white);
    client.sendCmd();
    usleep(500000);
    client.setAllLed(client.red);
    client.sendCmd();
    usleep(500000);
    client.setAllLed(client.green);
    client.sendCmd();
    usleep(500000);
    client.setAllLed(client.blue);
    client.sendCmd();
    usleep(500000);
    client.setAllLed(client.yellow);
    client.sendCmd();
    usleep(500000);
    client.setAllLed(client.black);
    client.sendCmd();

    return 0;
}
```

程序其实很好理解，就是各色的灯轮着亮一遍。

下面按照[官方教程](https://www.yuque.com/ironfatty/nly1un/cmls8h)的方法进行编译。

```sh
cd "Go1_Bot/FaceLightSDK"
mkdir build
cd build
cmake ..
make -j4
```

这其实就是`Go1_Bot/build_light_sdk.sh`中的内容。编译结束后，二进制程序将位于`bin`目录下。

运行一下程序测试：

```sh
./bin/faceLightClient
```

如果可以运行成功，后面在`python`程序中执行该函数就可以让狗子的灯点亮了！

```py
import os
os.system("<path-to-bin>/bin/faceLightClient")
```


