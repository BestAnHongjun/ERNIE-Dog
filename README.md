# ERNIE-Dog：基于文心一言大模型的机器狗

## 环境配置

### 1.创建虚拟环境

```sh
conda create -n ernie_dog python=3.10
conda activate ernie_dog
```

### 2.安装依赖项

```sh
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