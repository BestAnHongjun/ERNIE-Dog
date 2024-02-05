import os
import sys
import time
import math


class Dog:
    def __init__(self):
        current_directory = os.path.dirname(os.path.abspath(__file__))
        sys.path.append(os.path.join(current_directory, "..", "unitree_legged_sdk", "lib", "python", "arm64"))
        print(os.path.join(current_directory, "..", "unitree_legged_sdk", "lib", "python", "arm64"))
        import robot_interface as sdk

        HIGHLEVEL = 0xee
        LOWLEVEL  = 0xff
        self.udp = sdk.UDP(HIGHLEVEL, 8080, "192.168.123.161", 8082)
        self.cmd = sdk.HighCmd()
        self.state = sdk.HighState()
        
        self.udp.InitCmdData(self.cmd)
    
    def _init_cmd(self):
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
        # 1000个motiontime大约是50cm
        # 1m约是2000个motiontime
        motiontime = 0
        unit_move = 2000
        while True:
            time.sleep(0.002)
            motiontime = motiontime + 1

            self.udp.Recv()
            self.udp.GetRecv(self.state)

            self._init_cmd()

            if motiontime > 0 and motiontime < distance * unit_move:
                self.cmd.mode = 2
                self.cmd.gaitType = 1
                self.cmd.velocity = [0.2, 0] # -1  ~ +1
            
            if motiontime > distance * unit_move and motiontime < distance * unit_move + 1000:
                self.cmd.mode = 1

            if motiontime > distance * unit_move + 1000:
                break
            
            self.udp.SetSend(self.cmd)
            self.udp.Send()
    
    def turn(self, angle):
        # 500个motiontime大约是90度
        # 1度大约是500/90个motiontime
        motiontime = 0
        unit_angle = 500 / 90
        if angle > 0:
            direct = 1
            angle = angle
        else:
            direct = -1
            angle = -angle
        while True:
            time.sleep(0.002)
            motiontime = motiontime + 1

            self.udp.Recv()
            self.udp.GetRecv(self.state)

            self._init_cmd()

            if motiontime > 0 and motiontime < angle * unit_angle:
                self.cmd.mode = 2
                self.cmd.gaitType = 1
                self.cmd.yawSpeed = 2 * direct
            
            if motiontime > angle * unit_angle and motiontime < angle * unit_angle + 1000:
                self.cmd.mode = 1

            if motiontime > angle * unit_angle + 1000:
                break
            
            self.udp.SetSend(self.cmd)
            self.udp.Send()
        



if __name__ == "__main__":
    dog = Dog()
    dog.move_x(1)
