CURRENT_DIR=$(cd $(dirname $0); pwd)
cd "$CURRENT_DIR/CameraSDK"

mkdir build
cd build
cmake ..
make -j4