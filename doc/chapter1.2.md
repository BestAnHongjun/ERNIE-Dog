# 1.2 UnitreeCamera与PaddleOCR集成

关于PaddleOCR训练、量化、部署的详细教程可以参考[项目主页](https://github.com/PaddlePaddle/PaddleOCR)，本教程不再赘述。

本DEMO主要参考PaddleOCR项目的`tools/infer/predict_system.py`修改而来。你可以在PaddleOCR项目根目录下新建一个python文件：

```py
import cv2
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


if __name__ == "__main__":
    model = OCRModel()
    img = cv2.imread("./doc/imgs/00207393.jpg")

    res = model(img)
    print(res)
```

运行上述python脚本，便可以将`00207393.jpg`的OCR识别结果打印到屏幕。

不过在应用时，我们并不是推理本地图片，而是要推理`Nano1`发送来的图片流。请参考`PicSocket`[项目目录](https://gitee.com/an_hongjun/PicSocket)的`Python快速开始`安装好Python模块，然后使用如下方式接收图片流。

```py
import cv2
import picsocket


if __name__ == "__main__":
    # 监听8888端口
    img_receiver = picsocket.ImgReceiver(8888)

    while True:
        # 接收一帧
        img = img_receiver.read()

        # 可视化当前帧
        cv2.imshow("Demo", img)
        cv2.waitKey(5)
```

使用方法还是比较简明的，和`OpenCV`非常相似。

接下来咱们将`PicSocket`模块耦合进来，接收`Nano1`发来的图片流。

```py
import cv2
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


if __name__ == "__main__":
    model = OCRModel()

    # 用于接收Nano1发来的图片流
    img_receiver = picsocket.ImgReceiver(8888)
    
    while True:
        img = img_receiver.read() 
        # 图片原本是倒着的，翻转过来
        img = cv2.flip(img, -1)

        inp = input("---\n输入y,执行OCR;\n输入n,跳过该图片;\n输入其他内容,退出程序。\n[INPUT]>>> ")
        if inp == "n":
            continue
        elif inp == "y":
            dt_boxes, rec_res = model(img)

            # 将OCR结果拼接起来
            res_str = ""
            for text, score in rec_res:
                res_str += text
            res_str = res_str.replace("：", "；")
            if res_str[-1] != "。":
                res_str += "。"
            res_str = res_str.strip()

            # 打印OCR结果
            print(res_str)
        else:
            break
```

推理得到OCR结果后，需要将推理结果通过UDP协议发送给`Nano2`板卡。关于`Python`开发UDP程序的例子可以参考本教程的[3.2-如何调用狗子的扬声器](./chapter3.2.md)部分。

完整的`PaddleOCR`调用代码请见[demo_nano3_nx.py](../demo_nano3_nx.py)。