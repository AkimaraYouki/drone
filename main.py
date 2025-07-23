import pybullet as p
import pybullet_data
import pygame
import time

# ---------------- Initialization ----------------

def initialize_simulation():
    p.connect(p.GUI)
    p.setAdditionalSearchPath(pybullet_data.getDataPath())
    p.loadURDF("plane.urdf")

    p.setAdditionalSearchPath("gym-pybullet-drones/bullet3/data/Quadrotor")
    drone = p.loadURDF("quadrotor.urdf", [0, 0, 1])

    p.setGravity(0, 0, -10)

    prop_positions = [
        [0.175, 0, 0],
        [0, 0.175, 0],
        [-0.175, 0, 0],
        [0, -0.175, 0],
    ]

    return drone, prop_positions

def initialize_joystick():
    pygame.init()
    pygame.joystick.init()
    if pygame.joystick.get_count() == 0:
        raise RuntimeError("조이스틱이 연결되어 있지 않습니다.")
    joystick = pygame.joystick.Joystick(0)
    joystick.init()
    return joystick

# ---------------- Control Input ----------------

def get_joystick_input(joystick):
    pygame.event.pump()
    lx = joystick.get_axis(0)
    ly = -joystick.get_axis(1)  # 상하반전
    rx = joystick.get_axis(2)
    ry = joystick.get_axis(3)
    return lx, ly, rx, ry

# ---------------- Actuation ----------------

def apply_control(drone, prop_positions, thrust):
    for pos in prop_positions:
        p.applyExternalForce(
            objectUniqueId=drone,
            linkIndex=-1,
            forceObj=[0, 0, thrust],
            posObj=pos,
            flags=p.LINK_FRAME
        )

# ---------------- Main Loop ----------------

def main_loop():
    drone, prop_positions = initialize_simulation()
    joystick = initialize_joystick()

    try:
        while True:
            lx, ly, rx, ry = get_joystick_input(joystick)
            print(f"LX: {lx:.2f}, LY: {ly:.2f}, RX: {rx:.2f}, RY: {ry:.2f}")

            # 향후 제어기 로직은 여기에서 입력값 가공
            thrust = ly * 5  # 예: 단순 상하 thrust 비례 제어
            apply_control(drone, prop_positions, thrust)

            p.stepSimulation()
            time.sleep(1 / 240.0)

    except KeyboardInterrupt:
        p.disconnect()
        print("시뮬레이션 종료됨.")

# ---------------- Entry ----------------

if __name__ == "__main__":
    main_loop()