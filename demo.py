import os
import json
from ERNIE_Bot import Bot
from Go1_Bot.Dog import Dog


# 初始化文心一言大模型
token = os.getenv('ERNIE_BOT_TOKEN')
bot = Bot(token)

# 初始化Go1机器狗
dog = Dog(move=False)
name2func = {
    "move_x": dog.move_x,
    "move_y": dog.move_y,
    "turn": dog.turn,
    "light": dog.light,
    "beam": dog.beam
}

if __name__ == "__main__":
    command = '以初始位置为参考，你左前方30度方向、距离3m有一个红色的小球；右前方30度方向、距离1m有一个蓝色的小球；你正前方2m，有一个绿色的小球。请先走到蓝色的小球前面，叫一声，然后发出灯光。'
    print(" >>> 用户指令：", command, "\n")

    while True:
        ret, action = bot.get_actions(command)
        if ret:
            print(" <<< 文心大模型：", action["thoughts"])
            print("   - 调用方法：", action["name"])
            print("   - 调用参数：", action["arguments"])
        else:
            print(" <<< 文心大模型：", action)
            break
        
        # 本DEMO默认Bot返回结果正确，实际应用时请对参数正确性进行检查，并对异常情况做相应处理。
        func_call = name2func[action['name']]
        func_args = json.loads(action["arguments"])
        func_res = func_call(**func_args)
        print(" >>> 反馈：", func_res, "\n")
        
        command = func_res    
