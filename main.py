import pybullet as p
import time

import pybullet_data

# 물리 시뮬레이터 시작
p.connect(p.GUI)

# 중력 설정
p.setGravity(0, 0, -10)
p.setAdditionalSearchPath(pybullet_data.getDataPath())
# 바닥 생성
planeId = p.loadURDF("plane.urdf")

# 물체 생성
cubeId = p.loadURDF("cube.urdf", basePosition=[0,0,1])

# 시뮬레이션 실행
while True:
    p.stepSimulation()
    time.sleep(1./240.)


# p.disconnect()

