import pyspacemouse
import time

success = pyspacemouse.open(DeviceNumber=0)
if success:
    while 1:
        state = pyspacemouse.read()
        print(state.x, state.y, state.z)
        time.sleep(0.01)
