import copy, sys
import os, time
from tqdm import tqdm
import numpy as np
import pickle as pkl
import datetime
from absl import app, flags
from pynput import keyboard
from scipy.spatial.transform import Rotation as R

sys.path.append('/home/idm/zs/hil/hil-serl/')

# from experiments.mappings import CONFIG_MAPPING
from examples.experiments.mappings import CONFIG_MAPPING

FLAGS = flags.FLAGS
flags.DEFINE_string("exp_name", 'usb_pickup_insertion', "Name of experiment corresponding to folder.")
flags.DEFINE_integer("successes_needed", 200, "Number of successful transistions to collect.")
flags.DEFINE_integer("sim", 1, "0/1")


success_key = False
def on_press(key):
    global success_key
    try:
        if str(key) == 'Key.space':
            success_key = True
    except AttributeError:
        pass


def rotvec2quat(pos):
    rotvec = pos[3:]
    rotation = R.from_rotvec(rotvec)
    quat = rotation.as_quat()

    q = [pos[0] *1000, pos[1] *1000, pos[2] *1000] + list(quat)
    return pos

def quat2rotvec(pos):
    quat = pos[3:]
    rotation = R.from_quat(quat)
    rotvec = rotation.as_rotvec()
    q = [pos[0] / 1000, pos[1] / 1000, pos[2] / 1000]  + list(rotvec)
    return q

def main(_):
    global success_key
    listener = keyboard.Listener(
        on_press=on_press)
    listener.start()
    assert FLAGS.exp_name in CONFIG_MAPPING, 'Experiment folder not found.'
    config = CONFIG_MAPPING[FLAGS.exp_name]()
    env = config.get_environment(fake_env=False, save_video=False, classifier=False)

    sim = True
    if sim == False:
        import rtde_control, rtde_receive

        rtde_c = rtde_control.RTDEControlInterface("127.0.0.1")
        rtde_r = rtde_receive.RTDEReceiveInterface("127.0.0.1")


    obs, _ = env.reset()
    successes = []
    failures = []
    success_needed = FLAGS.successes_needed
    pbar = tqdm(total=success_needed)
    # print("success_needed = ", success_needed)
    while len(successes) < success_needed:
        actions = np.zeros(env.action_space.sample().shape)
        # 可以输出 actions
        actions, _ = env.action(actions)

        print("actions = ", actions)
        
        if sim == False:
            # 获取 ur 当前位姿
            pose = rtde_r.getActualTCPPose() # xyz+rotvec
            current_pose = rotvec2quat(pose)

            # 计算 ur 目标位姿        
            pos = env.get_target_robot_pose(actions, current_pose) # x y z qw qx qy qz
            pos = quat2rotvec(pos)

            # 控制 ur 运动
            rtde_c.moveL(pos, 0.5, 0.3)
        

if __name__ == "__main__":
    app.run(main)
