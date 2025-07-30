import cv2
import os
import time

# 저장 폴더 이름 및 생성
save_dir = "checkerboard_images"
os.makedirs(save_dir, exist_ok=True)

# 체커보드 내부 코너 수 (가로, 세로)
CHECKERBOARD = (9,6)  # 내부 코너 기준 (10x7 칸이면 (9,6))

# 카메라 초기화 (0: 기본 웹캠, PiCamera라면 `cv2.VideoCapture(0)` 그대로 가능)
cap = cv2.VideoCapture(0)

cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

# 저장 관련 변수
image_count = 0
MAX_IMAGES = 30

print("체커보드 자동 캡처 시작. 'q'를 눌러 중단하세요.")

while image_count < MAX_IMAGES:
    ret, frame = cap.read()
    if not ret:
        print("프레임을 가져오지 못했습니다.")
        continue

    cv2.imshow("Live Feed (press q to quit)", frame)

    key = cv2.waitKey(1) & 0xFF
    if key == ord('c'):  # 'c' 키를 눌러 저장
        filename = os.path.join(save_dir, f"img_{image_count:02d}.jpg")
        cv2.imwrite(filename, frame)
        print(f"[✔] 저장됨: {filename}")
        image_count += 1
    elif key == ord('q'):  # 'q' 키로 종료
        print("촬영 완료.")
        break
if cv2.waitKey(1) & 0xFF == ord('q'):
    print("촬영 완료.")
cap.release()
cv2.destroyAllWindows()