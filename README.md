# ERNIE-Dog：基于文心一言大模型的机器狗

## Go1-NX环境配置

### 1.创建虚拟环境

安装Miniconda。
> **关于为什么一定要装`Miniconda`**：调用文心一言`ERNIE-Bot`时需要安装`erniebot`包，该包要求的最低Python解释器版本为`Python>=3.8`，而`Go1-NX`预装的Python解释器版本为3.6，同时为了避免后续过程的其他麻烦（比如环境依赖冲突），因此安装`Miniconda`。*PS:有佬有其他solution可以用自己的方法，本`baseline`面向各水平广大群体。*

```sh
# 创建文件夹
mkdir -p ~/miniconda3

# 下载最新的Miniconda安装包
wget https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-aarch64.sh -O ~/miniconda3/miniconda.sh
```

> 如果在Go1板卡上遇到HTTPS证书相关问题问题，一般是由系统时间不准确导致的，执行如下指令自动同步系统时间：
```sh
sudo ntpdate ntp.aliyun.com
```

```sh
# 安装Miniconda
bash ~/miniconda3/miniconda.sh -b -u -p ~/miniconda3

# 删除安装包
rm -rf ~/miniconda3/miniconda.sh

# 初始化Miniconda环境
~/miniconda3/bin/conda init bash
source ~/.bashrc
```

这时你的命令行前面应该有小括号了`(base)`。

```sh
# 创建虚拟环境
conda create -n ernie_dog python=3.10

# 激活虚拟环境
conda activate ernie_dog
```
这时，命令行前面的小括号应该变成`(ernie_dog)`了，表示当前已经进入`ernie_dog`环境。

后面再执行相关代码时，记得确保在`ernie_dog`环境中。尤其是重启终端窗口之后，会默认以基础环境`base`启动。可参考以下命令：

```sh
# 创建新的虚拟环境
conda create -n <your-env-name> python=3.x

# 激活虚拟环境
conda activate <your-env-name>

# 退出虚拟环境
conda deactivate

# 删除虚拟环境
conda remove -n <your-env-name> --all # 慎用，不可逆！
```

### 2.下载仓库

```sh
# 下载到Home目录
cd ~

# 克隆Git仓库
git clone https://github.com/BestAnHongjun/ERNIE-Dog.git

# 如遇到网络问题，可由Gitee码云平台下载
# git clone https://gitee.com/an_hongjun/ERNIE-Dog.git
```

### 3.安装依赖项

```sh
cd ERNIE-Dog
pip install -r requirements.txt
```

### 1.下载宇树运动SDK

```sh
# 由GitHub拉取仓库
git clone https://github.com/unitreerobotics/unitree_legged_sdk.git

# 与本Demo保持一致版本
cd unitree_legged_sdk
git checkout 4539a6c10dfbc9781cea6fcb7d51bc6ddc6f71e1
```