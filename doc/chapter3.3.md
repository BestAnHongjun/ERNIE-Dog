# 3.3 控制狗子运动

阅读本教程之前请先阅读[官方文档教程-Go1 SDK HighLevel Interfaces](https://www.yuque.com/ironfatty/nly1un/kv5s7k)和[官方视频教程-使用unitree_legged_sdk控制宇树机器人](https://www.yuque.com/ironfatty/nly1un/su8o89)，了解相关基础知识。

Go1运动的官方开发SDK位于狗子树莓派板卡的`~/Unitree/SDK`目录下，本Baseline对其进行整理后放在了`Go1_Bot/LeggedSDK`目录下，基本没有做什么修改。

先介绍一下怎么编译`SDK`吧（`python`版本），在`conda`环境下进行编译时，如果按照官方的教程你可能会遇到一些莫名其妙的错误，主要原因是`CMake`在进行编译时会默认引用系统的`Python`解释器，而不是`conda`环境的解释器（要不是erniebot要求的`python`版本和预装的版本冲突了咱也不用兜这么多圈子是吧……）。

解决方案：在进行`cmake ..`时传入`Python`解释器的路径。

完成的编译命令如下：

```sh
# 安装依赖项
python -m pip install rospkg rospy catkin_tools

# 安装依赖项
sudo apt-get install libmsgpack-dev

# 进入SDK目录
cd "Go1_Bot/LeggedSDK"

mkdir build
cd build
cmake .. \
    -DPYTHON_BUILD=TRUE \
    -DPYTHON_EXECUTABLE=$(python -c "import sys; print(sys.executable)") \
    -DPYTHON_INCLUDE_DIR=$(python -c "from distutils.sysconfig import get_python_inc; print(get_python_inc())")  \
    -DPYTHON_LIBRARY=$(python -c "import distutils.sysconfig as sysconfig; print(sysconfig.get_config_var('LIBDIR'))")

make -j4
```

这些其实就是`build_legged_sdk.sh`中的内容。

编译完成后，在SDK目录的`lib/python`下应该会出现一个新的动态链接库，这就是编译好的`Python`库。

下面咱们就基于运动SDK，把在“2.3”章节说的五个元动作依次实现。在`Go1_Bot`目录下新建`Dog.py`，先初始化SDK：

```py
import os
import sys
import time
import math


class Dog:
    def __init__(self, move=True):
        # 把刚刚编译好的动态链接库所在目录加入系统环境变量
        self.current_directory = os.path.dirname(os.path.abspath(__file__))
        sys.path.append(os.path.join(self.current_directory, "LeggedSDK", "lib", "python", "arm64"))
        # 如果没有把编译好的动态链接库所在目录加入系统环境变量，import会失败
        import robot_interface as sdk

        HIGHLEVEL = 0xee
        LOWLEVEL  = 0xff
        # 下面的初始化操作是SDK的基操，看过官方教程应该就能理解
        # 更直接的，你可以参考一下`LeggedSDK/example_py/example_walk.py`
        self.udp = sdk.UDP(HIGHLEVEL, 8080, "192.168.123.161", 8082)
        self.cmd = sdk.HighCmd()
        self.state = sdk.HighState()
        self.move = move
        
        self.udp.InitCmdData(self.cmd)
    
    def _init_cmd(self):
        # 用于将cmd结构体清零
        self.cmd.mode = 0      # 0:idle, default stand      1:forced stand     2:walk continuously
        self.cmd.gaitType = 0
        self.cmd.speedLevel = 0
        self.cmd.footRaiseHeight = 0
        self.cmd.bodyHeight = 0
        self.cmd.euler = [0, 0, 0]
        self.cmd.velocity = [0, 0]
        self.cmd.yawSpeed = 0.0
        self.cmd.reserve = 0
```

下面，我们先来实现`move_x`元动作：

其实SDK实现控制狗子的思路非常简单，就是通过不断向下位机发送`cmd`状态包表明现在对狗子的期望状态。在编写运动时通常有一个循环体，还有一个计时器`motiontime`，每循环一次就对计时器增加一个单位。在循环体内，通过判断`motiontime`的大小，来决定狗子当前做什么动作。

对于`move_x`动作，如果说需要狗子向前运动1m，理论上来说，如果要运动精准的1m，我们是需要进行闭环控制的（依据惯导闭环/依据视觉闭环……），但是本baseline只是做一个演示，复杂的运动控制就交给你们懂控制的队友吧~

本baseline实现距离控制的思路是——计时！咱们基于统计学的原理，经过大量试验样本发现，在0.2的平移速度下，狗子运动1000个motiontime的时间所经过的距离大约是50厘米！那么，如果我们想要狗子平移x米，只需要让他运动x*2000个motiontime！！！

> PS: 其实作者非常懒，“大量试验”的样本容量为1，但是作为教程咱们需要“严谨”，于是披上一层“科学的外衣”……大佬们自己写PID吧~

```py
def move_x(self, distance):
    # 1000个motiontime大约是50cm
    # 1m约是2000个motiontime
    motiontime = 0
    unit_move = 2000
    if distance > 0:
        direct = 1
        distance = distance
        feedback = "已沿x轴向前移动{}m。".format(distance)
    else:
        direct = -1
        distance = -distance
        feedback = "已沿x轴向后移动{}m。".format(distance)
    while self.move:
        time.sleep(0.002)
        motiontime = motiontime + 1

        self.udp.Recv()
        self.udp.GetRecv(self.state)

        self._init_cmd()

        if motiontime > 0 and motiontime < distance * unit_move:
            self.cmd.mode = 2
            self.cmd.gaitType = 1
            self.cmd.velocity = [0.2 * direct, 0] # -1  ~ +1
        
        # 这一个时间区间是用来状态缓冲的，避免狗子状态突变，引发别狗腿等问题……
        if motiontime > distance * unit_move and motiontime < distance * unit_move + 1000:
            self.cmd.mode = 1

        if motiontime > distance * unit_move + 1000:
            break
        
        self.udp.SetSend(self.cmd)
        self.udp.Send()

    # 反馈一个字符串，将来发送给文心大模型
    return feedback
```

其他的元动作的实现也是相似的，教程就不说废话了，佬们自己去看[Dog.py](../Go1_Bot/Dog.py)吧~
