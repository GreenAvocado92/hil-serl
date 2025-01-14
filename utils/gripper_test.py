import subprocess, re

"""
# init
bash_command = 'ros2 topic pub --once /f3_control_topic program_interfaces/msg/Fingercontrol "{sign: 1, senddata: 1}"'
result = subprocess.run(bash_command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)

# close
bash_command = 'ros2 topic pub --once /f3_control_topic program_interfaces/msg/Fingercontrol "{sign: 2, senddata: 1}"'
result = subprocess.run(bash_command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)

# open
bash_command = 'ros2 topic pub --once /f3_control_topic program_interfaces/msg/Fingercontrol "{sign: 3, senddata: 1}"'
result = subprocess.run(bash_command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)

"""

cmd = 'ros2 topic  echo --once  /Robotiq3FGripperRobotInput'
result = subprocess.run(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
res = result.stdout.split("\n")
print(res)
# g_sta = int(res[4][-1])
# print("g_sta = ", g_sta)
