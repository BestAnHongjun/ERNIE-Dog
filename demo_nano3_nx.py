import os
import sys
import cv2
import time
import socket
import picsocket
import tools.infer.utility as utility
from tools.infer.predict_system import TextSystem


class OCRModel:
    def __init__(self, det_model_dir=None, rec_model_dir=None):
        if det_model_dir is None:
            det_model_dir = "./pretrain_models/ch_PP-OCRv3_det_infer/"
        if rec_model_dir is None:
            rec_model_dir = "./pretrain_models/ch_PP-OCRv3_rec_infer/"
        args = utility.parse_args()
        args.det_model_dir = det_model_dir
        args.rec_model_dir = rec_model_dir
        self.text_sys = TextSystem(args)

    def __call__(self, img):
        dt_boxes, rec_res, _ = self.text_sys(img)
        return dt_boxes, rec_res


def send_to_nano2(text):
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    addr = ("192.168.123.14", 8889)
    s.sendto(text.encode(), addr)
    time.sleep(1)
    s.close()


if __name__ == "__main__":
    model = OCRModel()
    img = cv2.imread("./doc/imgs/00207393.jpg")

    # 用于接收Nano1发来的图片流
    img_receiver = picsocket.ImgReceiver(8888)
    # 新建一个sender，转发到你的linux主机，用于调试
    img_sender = picsocket.ImgSender("192.168.123.100", 8888)
    
    while True:
        img = img_receiver.read() 
        # 图片原本是倒着的，翻转过来
        img = cv2.flip(img, -1)
        img_sender.send(img)

        inp = input("---\n输入y,执行OCR;\n输入n,跳过该图片;\n输入其他内容,退出程序。\n[INPUT]>>> ")
        if inp == "n":
            continue
        elif inp == "y":
            dt_boxes, rec_res = model(img)
            res_str = ""
            for text, score in rec_res:
                res_str += text
            res_str = res_str.replace(":", "；")
            if res_str[-1] != "。":
                res_str += "。"
            res_str = res_str.strip()
            inp = input("---\nOCR结果：{}\n输入y,将该结果发送给文心一言;\n输入n,跳过该结果;\n输入其他内容,退出程序。\n[INPUT]>>> ".format(res_str))
            if inp == "n":
                continue 
            elif inp == "y":
                send_to_nano2(res_str)
                print("已发送。")
            else:
                break
        else:
            break

    # res = model(img)
    # print(res)
