import erniebot


class Bot:
    def __init__(self, token: str, system: str=None):
        erniebot.api_type = "aistudio"
        erniebot.access_token = token 
        print("载入token:", token, "\n")
        if system is None:
            self.system = '你是一只机器狗，你有move_x、move_y、turn、beam、light五个元动作，可以在平面内沿x轴或y轴平移，向左或向右旋转，发出灯光，或发出声音。当你想去一个位置，你需要先结合目标所在的方位，旋转[turn]一定角度对准下一个位置，然后向前平移[move]到下一个位置。如果让你发出声音，你要调用[beam]。如果让你发出灯光，你要调用[light]。'
        else:
            self.system = system

        self.functions = [
            self.turn_desc(),
            self.move_x_desc(),
            self.move_y_desc(),
            self.beam_desc(),
            self.light_desc()
        ]
        self.messages = []
    
    def get_actions(self, message):
        if isinstance(message, str):
            message = {'role': 'user', 'content': message}
        self.messages.append(message)

        create_kwargs = {
            'model': 'ernie-3.5',
            'messages': self.messages,
            'system': self.system,
            'functions': self.functions,
            'top_p': 0  # 减少随机性，使结果可复现。
        }

        response = erniebot.ChatCompletion.create(**create_kwargs)

        if response.is_function_response:
            # 模型建议调用函数
            function_call = response.get_result()
            self.messages.append(response.to_message())
            return True, function_call
        else:
            # 模型返回普通的文本消息
            result = response.get_result()
            self.messages.append(response.to_message())
            return False, result

    @staticmethod
    def move_x_desc():
        desc = {
            'name': 'move_x',
            'description': '沿相对此刻的x轴方向移动一定的距离。',
            'parameters': {
                'type': 'object',
                'properties': {
                    'distance': {
                        'type': 'integer',
                        'description': '沿x轴平移的距离，单位为米。大于0向正前方平移，小于0向正后方平移。',
                        'minimum': -50,
                        'maximum': 50
                    }
                },
                'required': ['distance']
            }
        }
        return desc
    
    @staticmethod
    def move_y_desc():
        desc = {
            'name': 'move_y',
            'description': '沿相对此刻的y轴方向移动一定的距离。',
            'parameters': {
                'type': 'object',
                'properties': {
                    'distance': {
                        'type': 'integer',
                        'description': '沿y轴平移的距离，单位为米。大于0向正左方平移，小于0向正右方平移。',
                        'minimum': -50,
                        'maximum': 50
                    }
                },
                'required': ['distance']
            }
        }
        return desc
    
    @staticmethod
    def turn_desc():
        desc = {
            'name': 'turn',
            'description': '以自我为中心旋转一定的角度。',
            'parameters': {
                'type': 'object',
                'properties': {
                    'angle': {
                        'type': 'integer',
                        'description': '旋转的角度，单位为度。大于0向右转，小于0向左转。',
                        'minimum': -90,
                        'maximum': 90
                    }
                },
                'required': ['angle']
            }
        }
        return desc
    
    @staticmethod
    def light_desc():
        desc = {
            'name': 'light',
            'description': '发出灯光。',
            'parameters': {
                'type': 'object',
                'properties': {
                    'arg': {
                        'type': 'integer',
                        'description': '本函数没有参数，请恒给0。',
                    }
                }
            }
        }
        return desc

    @staticmethod
    def beam_desc():
        desc = {
            'name': 'beam',
            'description': '发出声音。',
            'parameters': {
                'type': 'object',
                'properties': {
                    'arg': {
                        'type': 'integer',
                        'description': '本函数没有参数，请恒给0。',
                    }
                }
            }
        }
        return desc


if __name__ == "__main__":
    # for test
    import os
    token = os.getenv('ERNIE_BOT_TOKEN') # 通过环境变量方式获取token
    bot = Bot(token)

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
        
        command = "已完成以上动作"
        print(" >>> 反馈：", command, "\n")
