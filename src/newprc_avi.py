import cv2
import numpy as np
import math

# 각 파일 path
protoFile = "pose_deploy_linevec_faster_4_stages.prototxt"
weightsFile = "pose_iter_160000.caffemodel"

BODY_PARTS = {"Head": 0, "Neck": 1, "RShoulder": 2, "RElbow": 3, "RWrist": 4,
              "LShoulder": 5, "LElbow": 6, "LWrist": 7, "RHip": 8, "RKnee": 9,
              "RAnkle": 10, "LHip": 11, "LKnee": 12, "LAnkle": 13, "Chest": 14,
              "Background": 15}

POSE_PAIRS = [["Head", "Neck"], ["Neck", "RShoulder"], ["RShoulder", "RElbow"],
              ["RElbow", "RWrist"], ["Neck", "LShoulder"], ["LShoulder", "LElbow"],
              ["LElbow", "LWrist"], ["Neck", "Chest"], ["Chest", "RHip"], ["RHip", "RKnee"],
              ["RKnee", "RAnkle"], ["Chest", "LHip"], ["LHip", "LKnee"], ["LKnee", "LAnkle"]]

# OpenCV DNN 모듈 초기화
net = cv2.dnn.readNetFromCaffe(protoFile, weightsFile)

# 동영상 파일 열기
video_file = "run_final.avi"
cap = cv2.VideoCapture(video_file)
fail_count = 0
while True:
    # 프레임 읽기
    ret, frame = cap.read()

    if not ret:
        break

    # 입력 이미지 크기 조정
    height, width = frame.shape[:2]
    inWidth = 368
    inHeight = 368
    net.setInput(cv2.dnn.blobFromImage(frame, 1.0/255, (inWidth, inHeight), (127.5, 127.5, 127.5), swapRB=False, crop=False))

    # 예측 수행
    out = net.forward()

    # 각 관절의 좌표 추출
    points = []
    for i in range(len(BODY_PARTS)-1):
        probMap = out[0, i, :, :]
        minVal, prob, minLoc, point = cv2.minMaxLoc(probMap)
        x = int((width * point[0]) / out.shape[3])
        y = int((height * point[1]) / out.shape[2])
        if prob > 0.1 :    
            cv2.circle(frame, (x, y), 3, (0, 255, 255), thickness=-1, lineType=cv2.FILLED)       # circle(그릴곳, 원의 중심, 반지름, 색)
            cv2.putText(frame, "{}".format(i), (x, y), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 1, lineType=cv2.LINE_AA)
            points.append((x, y))
        else :
            points.append(None)

        #points.append((x, y))

    # 각 관절에 점 표시
    for point in points:
        cv2.circle(frame, point, 5, (0, 255, 0), -1)
    # 왼쪽 관절을 연결하여 선 그리기
    for pair in [(11, 12), (12, 13)]:
        partA = pair[0]
        partB = pair[1]
        if points[partA] and points[partB]:
            cv2.line(frame, points[partA], points[partB], (0, 255, 255), 2)

    # 오른쪽 관절을 연결하여 선 그리기
    for pair in [(8, 9), (9, 10)]:
        partA = pair[0]
        partB = pair[1]
        if points[partA] and points[partB]:
            cv2.line(frame, points[partA], points[partB], (0, 255, 255), 2)

    # 오른쪽 다리 각도 계산
    angle_deg_r = 0
    if points[8] != None and points[9] != None and points[10] != None:
        dx1 = points[8][0] - points[9][0]
        dy1 = points[8][1] - points[9][1]
        dx2 = points[10][0] - points[9][0]
        dy2 = points[10][1] - points[9][1]
        angle_rad_r = math.atan2(dy1*dx2 - dx1*dy2, dx1*dx2 + dy1*dy2)

    # 라디안을 도(degree)로 변환
        angle_deg_r = math.degrees(angle_rad_r)

    # 음수일 경우 양수로 변환
        if angle_deg_r < 0:
            angle_deg_r += 360.0
    # 왼쪽 다리 각도 계산
    angle_deg_l = 0
    if points[11] != None and points[12] != None and points[13] != None:
        dx3 = points[11][0] - points[12][0]
        dy3 = points[11][1] - points[12][1]
        dx4 = points[13][0] - points[12][0]
        dy4 = points[13][1] - points[12][1]
        angle_rad_l = math.atan2(dy3*dx4 - dx3*dy4, dx3*dx4 + dy3*dy4)

    # 라디안을 도(degree)로 변환
        angle_deg_l = math.degrees(angle_rad_l)

    # 음수일 경우 양수로 변환
        if angle_deg_l < 0:
            angle_deg_l += 360.0    
    # 각도가 일정 범위를 벗어나면 경고 출력
    if (angle_deg_l > 210 or angle_deg_l < 150) and angle_deg_l != 0:
        cv2.putText(frame, "Alert: Left leg is not Straight", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
    if (angle_deg_r > 210 or angle_deg_r < 150) and angle_deg_r != 0:
        cv2.putText(frame, "Alert: Right leg is not Straight", (10, 60), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
    if (angle_deg_l > 210 or angle_deg_l < 150) and angle_deg_l != 0 \
        and (angle_deg_r > 210 or angle_deg_r < 150) and angle_deg_r != 0:
            fail_count += 1
    cv2.putText(frame, "Fail Count : %d" %fail_count, (10, 90), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
    # 화면에 출력
    cv2.imshow("Pose Detection", frame)
    cv2.waitKey(25) 

    # 종료 조건
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# 동영상 파일과 윈도우 닫기
cap.release()
cv2.destroyAllWindows()