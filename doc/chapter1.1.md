# 1.1 UnitreeCamera SDK教程

阅读本教程之前请先阅读[官方教程-Go1双目鱼眼相机的开发使用](https://www.yuque.com/ironfatty/nly1un/rguxgz)，了解相关基础知识。

Go1头部灯带的官方开发SDK位于狗子Nano1-3板卡的`~/Unitree/SDK`目录下，本Baseline对其进行整理后放在了`Go1_Bot/CameraSDK`目录下，主要对`CMakeLists.txt`做了相关修改，并添加了`ERNIE_Dog_nano1.cpp`。

咱们的`DEMO`基本参考官方的[example_getRectFrame.cc](../Go1_Bot/CameraSDK/examples/example_getRectFrame.cc)编写，获取畸变矫正后的图像。

首先引入头文件。

```cpp
#include <UnitreeCameraSDK.hpp>
#include <unistd.h>
#include <cstdlib>
```

下面编写`main`函数。如果你认真看过官方教程的话，每次运行`CameraSDK`程序之前都需要做一步操作：杀进程！为了省事，咱们直接把杀进程的命令写进`main`函数。

```cpp
int main(){
    // 杀进程
    system("ps -aux | grep point_cloud_node | awk '{print $2}' | xargs kill -9");
    system("ps -aux | grep mqttControlNode | awk '{print $2}' | xargs kill -9");
    system("ps -aux | grep live_human_pose | awk '{print $2}' | xargs kill -9");
    system("ps -aux | grep rosnode | awk '{print $2}' | xargs kill -9");
}
```

下面我们创建`UnitreeCamera`实例。如果你看过[官方DEMO](../Go1_Bot/CameraSDK/examples/example_getRectFrame.cc)的话，它在创建实例的时候，是通过读取[stereo_camera_config.yaml]这个配置文件来配置相关参数的。

**笔者表示，感觉好难用……**

咱们来看一下[UnitreeCameraSDK.hpp](../Go1_Bot/CameraSDK/include/UnitreeCameraSDK.hpp)，第`66`行有个函数你看见没！！

```cpp
UnitreeCamera(int deviceNode);
```

这不有通过设备号直接声明的方法吗！就和`OpenCV`的那个`VideoCapture`似的。有这么简洁的方法为何不用！！！

查一下[官方文档](https://www.yuque.com/ironfatty/nly1un/rguxgz)，前部摄像头的设备号是1。

OK，咱们来声明前部摄像头的实例。

```cpp
int deviceNode = 1; ///< default 1 -> /dev/video1
cv::Size frameSize(1856, 800); ///< default frame size 1856x800
int fps = 30; ///< default camera fps: 30

UnitreeCamera cam(deviceNode); ///< init camera by device node number
if(!cam.isOpened())   ///< get camera open state
    exit(EXIT_FAILURE);
```

以及配置相关参数，都是按照[官方DEMO](../Go1_Bot/CameraSDK/examples/example_getRectFrame.cc)来的。

```cpp
cam.setRawFrameSize(frameSize); ///< set camera frame size
cam.setRawFrameRate(fps);       ///< set camera camera fps
cam.setRectFrameSize(cv::Size(frameSize.width >> 2, frameSize.height >> 1)); ///< set camera rectify frame size
cam.startCapture(); ///< disable image h264 encoding and share memory sharing
```

下面就是咱们的主循环了，获取前部双目相机经过畸变矫正的图像。`left`是左目，`right`是右目。

```cpp
usleep(500000);
while(cam.isOpened()){
    cv::Mat left,right;
    if(!cam.getRectStereoFrame(left,right)){ ///< get rectify left,right frame  
        usleep(1000);
        continue;
    }
}
```

大家有用过`OpenCV`写过读取摄像头图像的经历的话，代码逻辑都很相似，应该不难理解。

**But！！！问题来了！！！**

* 宇树官方的`CameraSDK`只提供了`C++`版本；
* 咱们的下游任务要用`PaddleOCR`做，只提供了`Python`版本；
* 前部摄像头连接在`Nano1`上，因此必须在`Nano1`上运行`SDK`读摄像头。但是`PaddleOCR`为了推理实时性，要部署在`NX`上，不在同一个设备。

也就是说，咱们需要一个**跨语言**的、**跨平台**的局域网图传。

恶心不？哈哈，孩子还是参赛选手的时候被这问题恶心了可不止一年。

笔者本来打算在这个Baseline教程里面讲这图传该咋写的……emmm但是涉及的内容又有些偏离主题，好像又有些超纲。

于是笔者整理了一下之前参赛用的图传代码，给大家造个轮子，倾情献上：**PicSocket**！！

* 支持**跨语言**，封装了C/C++和Python的接口；
* 支持**跨平台**，windows/Linux/MacOS/Jetson/树莓派/香橙派……
* 目前还是beta版本，不过针对狗子平台已经调通了。佬们如果在其他平台部署遇到了问题，或者遇到了什么bug，欢迎提issue。

GitHub地址：https://github.com/BestAnHongjun/PicSocket
Gitee地址：https://gitee.com/an_hongjun/PicSocket

佬，看在孩子被恶心了那么久还给大伙造轮子的份上就给个star吧。

具体的使用教程可以参考[项目主页](https://gitee.com/an_hongjun/PicSocket)。下面咱们把`PicSocket`加入到咱们的代码中。

```cpp
// 引入头文件
#include "pic_socket.h"

// 声明发送端，目标地址192.168.123.15:8888
UDPImgSender img_sender("192.168.123.15", 8888);

// 发送OpenCV格式的帧
img_sender.send(left);
```

用法还算简洁吧，集成到代码中最终长这样：

```cpp
/*
 * Copyright (C) 2024 Coder.AN
 * Email: an.hongjun@foxmail.com
 * Page: www.anhongjun.top
 */

#include <UnitreeCameraSDK.hpp>
#include <unistd.h>
#include <cstdlib>

#include "pic_socket.h"

int main(){
    // 杀进程
    system("ps -aux | grep point_cloud_node | awk '{print $2}' | xargs kill -9");
    system("ps -aux | grep mqttControlNode | awk '{print $2}' | xargs kill -9");
    system("ps -aux | grep live_human_pose | awk '{print $2}' | xargs kill -9");
    system("ps -aux | grep rosnode | awk '{print $2}' | xargs kill -9");
    
    int deviceNode = 1; ///< default 1 -> /dev/video1
    cv::Size frameSize(1856, 800); ///< default frame size 1856x800
    int fps = 30; ///< default camera fps: 30
    
    UnitreeCamera cam(deviceNode); ///< init camera by device node number
    if(!cam.isOpened())   ///< get camera open state
        exit(EXIT_FAILURE);
    
    cam.setRawFrameSize(frameSize); ///< set camera frame size
    cam.setRawFrameRate(fps);       ///< set camera camera fps
    cam.setRectFrameSize(cv::Size(frameSize.width >> 2, frameSize.height >> 1)); ///< set camera rectify frame size
    cam.startCapture(); ///< disable image h264 encoding and share memory sharing

    UDPImgSender img_sender("192.168.123.15", 8888);
    
    usleep(500000);
    while(cam.isOpened()){
        cv::Mat left,right;
        if(!cam.getRectStereoFrame(left,right)){ ///< get rectify left,right frame  
            usleep(1000);
            continue;
        }

        img_sender.send(left);
    }
    
    cam.stopCapture(); ///< stop camera capturing
    
    return 0;
}
```

这就是[ERNIE_Dog_nano1.cpp](../Go1_Bot/CameraSDK/ERNIE_Dog_nano1.cpp)中的内容。

下面咱们来编译代码。

```sh
cd ~/ERNIE-Dog/Go1_Bot/CameraSDK
mkdir build
cd build
cmake ..
make -j4
```

以上就是[build_camera_sdk.sh](../Go1_Bot/build_camera_sdk.sh)的内容。编译完成后，二进制程序会输出到`bins`文件夹。

执行该二进制文件，即可将图片流图送到`192.168.123.15:8888`。

你可以在你自己的电脑上(最好是Linux)，仿照[PicSocket教程](https://gitee.com/an_hongjun/PicSocket)的快速开始部分在本地安装python模块，然后修改发送端的ip地址及端口指向你的电脑，然后在你的电脑上运行[picsocket_receiver.py](https://gitee.com/an_hongjun/PicSocket/blob/v0.0.1/example/python/picsocket_receiver.py)，就可以方便的查看狗子第一视角的图像了。
