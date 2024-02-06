echo "即将通过apt安装libmsgpack-dev包,可能需要输入密码。"
sudo apt-get install libmsgpack-dev

CURRENT_DIR=$(cd $(dirname $0); pwd)
cd "$CURRENT_DIR/LeggedSDK"

mkdir build
cd build
cmake .. \
    -DPYTHON_BUILD=TRUE \
    -DPYTHON_EXECUTABLE=$(python -c "import sys; print(sys.executable)") \
    -DPYTHON_INCLUDE_DIR=$(python -c "from distutils.sysconfig import get_python_inc; print(get_python_inc())")  \
    -DPYTHON_LIBRARY=$(python -c "import distutils.sysconfig as sysconfig; print(sysconfig.get_config_var('LIBDIR'))")
make -j4
