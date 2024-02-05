import json
from ERNIE_Bot import Bot


def move_x(distance):
    feedback = "已沿x轴移动{}m。".format(distance)
    print(feedback)
    return feedback

def move_y(distance):
    feedback = "已沿y轴移动{}m。".format(distance)
    print(feedback)
    return feedback

def turn(angle):
    feedback = "已旋转{}度。".format(angle)
    print(feedback)
    return feedback

def light(arg):
    feedback = "已发出灯光。"
    print(feedback)
    return feedback

def beam(arg):
    feedback = "已发出声音。"
    print(feedback)
    return feedback

name2func = {
    "move_x": move_x,
    "move_y": move_y,
    "turn": turn,
    "light": light,
    "beam": beam
}

if __name__ == "__main__":
    token = ''
    command = '以初始位置为参考，你左前方30度方向、距离10m有一个红色的小球；右前方30度方向、距离3m有一个蓝色的小球；你正前方8m，有一个绿色的小球。请先走到蓝色的小球前面，叫一声，然后发出灯光。'

    bot = Bot(token)
    while True:
        ret, action = bot.get_actions(command)
        print(action)
        if not ret: break 

        # 本DEMO默认Bot返回结果正确，实际应用时请对参数正确性进行检查，并对异常情况做相应处理。
        func_call = name2func[action['name']]
        func_args = json.loads(action["arguments"])
        func_res = func_call(**func_args)
        
        command = func_res    
