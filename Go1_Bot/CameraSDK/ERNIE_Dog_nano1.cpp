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
