import erniebot


class Bot:
    def __init__(self, token: str, system: str=None):
        erniebot.api_type = "aistudio"
        erniebot.access_token = token 
        if system is None:
            self.system = '你是一只机器狗，你有move_x、move_y、turn、beam、light五个元动作，可以在平面内沿x轴或y轴平移，向左或向右旋转，发出灯光或发出声音。当你想去一个位置，你需要先旋转角度对准下一个位置，然后向前平移到下一个位置。旋转角度时，注意角度的正负号，向左转是负的，向右转是正的。'
        else:
            self.system = system

        self.functions = [
            self.turn_desc(),
            self.move_x_desc(),
            self.move_y_desc(),
            self.light_desc(),
            self.beam_desc(),
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
            'functions': self.functions
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
                        'description': '沿x轴平移的距离，单位为厘米。大于0向正前方平移，小于0向正后方平移。',
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
                        'description': '沿y轴平移的距离，单位为厘米。大于0向正左方平移，小于0向正右方平移。',
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
                        'description': '旋转的角度，单位为度。大于0向左转，小于0向右转。',
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
