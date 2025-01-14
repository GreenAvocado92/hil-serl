from flask import Flask, request
from gevent import pywsgi
import os, logging, sys, argparse
import base64, json
import datetime, logging, math
from ctypes import *
from scipy.spatial.transform import Rotation as R
import numpy as np
import requests, subprocess

app = Flask(__name__)

import rtde_receive, rtde_control
rtde_r = rtde_receive.RTDEReceiveInterface("192.168.8.12")
rtde_c = rtde_control.RTDEControlInterface("192.168.8.12")

@app.route("/clearerr", methods=['POST'])
def GenerateP0Demo():
    logger.info("start clearerr ...")
    # param = request.get_json()
    return {"res": 1}

def rotvec2quat(pos):
    rotvec = pos[3:6]
    rotation = R.from_rotvec(rotvec)
    quat = rotation.as_quat()

    q = [pos[0] *1000, pos[1] *1000, pos[2] *1000] + list(quat)
    return q

def quat2rotvec(pos):
    quat = pos[3:]
    rotation = R.from_quat(quat)
    rotvec = rotation.as_rotvec()
    q = [pos[0] / 1000, pos[1] / 1000, pos[2] / 1000]  + list(rotvec)
    return q

@app.route("/pose", methods=['POST'])
def move_robot_pose():
    print("start pose ...")
    param = request.get_json()
    target_pos = param['arr']

    target_pos = quat2rotvec(target_pos)
    # print("=====================")
    # print("cur_pos = ", rtde_r.getActualTCPPose())
    # print("cur_quat= ", rotvec2quat(rtde_r.getActualTCPPose()))
    # print("tar_pos = ", target_pos)
    # 控制 ur 运动
    rtde_c.moveL(target_pos, 0.5, 0.3)
    
    return {"res": 1}



@app.route("/getstate", methods=['POST'])
def ur10e_getstate():
    print("get ur10e state ...")
    sim = False
    ps = {}
    if sim == False:
        pose = rtde_r.getActualTCPPose()
        pose = rotvec2quat(pose)
        joint = rtde_r.getActualQ()
        force = rtde_r.getActualTCPForce()
        force = list(force)
        joint_speed = rtde_r.getActualQd()
        pose_speed = rtde_r.getActualTCPSpeed()

        ps['pose'] = list(pose)
        ps['vel'] = list(pose_speed)
        ps['force'] = force[:3]
        ps['torque'] = force[3:]
        ps['gripper_pos'] = 0

        # get gripper current status
        # cmd = 'ros2 topic  echo --once  /Robotiq3FGripperRobotInput'
        # result = subprocess.run(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        # res = result.stdout.split("\n")
        # g_sta = int(res[4][-1])
        # gripper_status = 1
        # if g_sta !=2 and g_sta != 3: # gripper is closed
        #     gripper_status = -1
        # if g_sta !=3:
        #     gripper_status = 1
        # ps['gripper_pos'] = gripper_status # -1 表示关闭状态
    else:
        ps['pose'] = [1,2,3,4,5,6,7]
        ps['vel'] = [1,2,3,4,5,6]
        ps['force'] = [1,2,3]
        ps['torque'] = [1,2,3]
        ps['gripper_pos'] = -1 # 可能是-1和1，表示夹具的开闭状态
    return ps

@app.route("/init_gripper", methods=['POST'])
def init_gripper():
    bash_command = 'ros2 topic pub --once /f3_control_topic program_interfaces/msg/Fingercontrol "{sign: 1, senddata: 1}"'
    result = subprocess.run(bash_command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    return {'res': 1}

@app.route("/close_gripper", methods=['POST'])
def close_gripper():
    bash_command = 'ros2 topic pub --once /f3_control_topic program_interfaces/msg/Fingercontrol "{sign: 2, senddata: 1}"'
    result = subprocess.run(bash_command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    return {'res': 1}

@app.route("/open_gripper", methods=['POST'])
def open_gripper():
    bash_command = 'ros2 topic pub --once /f3_control_topic program_interfaces/msg/Fingercontrol "{sign: 3, senddata: 1}"'
    result = subprocess.run(bash_command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    return {'res': 1}

if __name__ == '__main__':
    logger = logging.getLogger()
    logger.setLevel(logging.DEBUG)

    # 创建FileHandler对象
    fh = logging.FileHandler('log.log')
    fh.setLevel(logging.DEBUG)
    # 创建Formatter对象
    formatter = logging.Formatter('%(asctime)s[%(levelname)s]: %(message)s')
    fh.setFormatter(formatter)
    # 将FileHandler对象添加到Logger对象中
    logger.addHandler(fh)

    # 记录日志信息
    logger.info('start server ...')
    server = pywsgi.WSGIServer(('127.0.0.1', 5001), app)
    server.serve_forever()