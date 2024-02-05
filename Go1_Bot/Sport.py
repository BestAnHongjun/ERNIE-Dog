import os
import sys
import time
import math


class Dog:
    def __init__(self):
        current_directory = os.path.dirname(os.path.abspath(__file__))
        sys.path.append(os.path.join(current_directory, "..", "unitree_legged_sdk", "lib", "python", "arm64"))
        import robot_interface as sdk

        HIGHLEVEL = 0xee
        LOWLEVEL  = 0xff
        self.udp = sdk.UDP(HIGHLEVEL, 8080, "192.168.123.161", 8082)
        self.cmd = sdk.HighCmd()
        self.state = sdk.HighState()
        
        self.udp.InitCmdData(cmd)
    
    def _init_cmd():
        self.cmd.mode = 0      # 0:idle, default stand      1:forced stand     2:walk continuously
        self.cmd.gaitType = 0
        self.cmd.speedLevel = 0
        self.cmd.footRaiseHeight = 0
        self.cmd.bodyHeight = 0
        self.cmd.euler = [0, 0, 0]
        self.cmd.velocity = [0, 0]
        self.cmd.yawSpeed = 0.0
        self.cmd.reserve = 0
    
    def move_x(self, distance):
        motiontime = 0
        while True:
            time.sleep(0.002)
            motiontime = motiontime + 1

            udp.Recv()
            udp.GetRecv(state)

            self._init_cmd()

            if motiontime > 0 and motiontime < distance * 1000:
                cmd.mode = 2
                cmd.gaitType = 1
                cmd.velocity = [0.2, 0] # -1  ~ +1
            
            if motiontime > distance * 1000 and motiontime < distance * 1000 + 1000:
                cmd.mode = 1

            if motiontime > distance * 1000 + 1000:
                break
            
            udp.SetSend(cmd)
            udp.Send()
        



if __name__ == "__main__":
    dog = Dog()
    dog.move_x(0.5)
