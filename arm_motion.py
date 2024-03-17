import time

from sic_framework.devices.common_naoqi.naoqi_motion import NaoqiIdlePostureRequest
from sic_framework.devices.common_naoqi.naoqi_motion_recorder import StartRecording, StopRecording, PlayRecording, NaoqiMotionRecorderConf, NaoqiMotionRecording
from sic_framework.devices.common_naoqi.naoqi_stiffness import Stiffness
from sic_framework.devices import Nao

nao = Nao("192.168.1.100")

# Only parts mentioned below will be moved
chain = ["RArm"]

# Set stiffness of the arm to zero
nao.motion.request(NaoqiIdlePostureRequest("Body", False))
nao.stiffness.request(Stiffness(0.0, chain))

'''
If you want to create your own motion (motion has to be done in 5 seconds)

print("Starting to record in one second!")
time.sleep(1)

nao.motion_record.request(StartRecording(chain))
print("Start moving the robot!")

record_time = 5
time.sleep(record_time)

recording = nao.motion_record.request(StopRecording())

# save the recording to a file
recording.save("wave.motion")
print("Done")
'''


recording = NaoqiMotionRecording.load("wave.motion")

# set stiffness to allow the robot to move the arm
nao.stiffness.request(Stiffness(.95, chain))
nao.motion_record.request(PlayRecording(recording))
nao.stiffness.request(Stiffness(.0, chain))
