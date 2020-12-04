#!/usr/bin/env python
# -*- coding: utf-8 -*-
import tello		# tello.py 가져오기
import time			# time.sleep를 사용하고 싶기 때문에
import cv2			# OpenCV를 사용하기 위해서 

# 메인 함수
def main():
	# Tello 클래스를 써서 drone이라는 instance(실체)를 만든다.
	drone = tello.Tello('', 8889, command_timeout=.01)  

	current_time = time.time()	# 현재 시각의 저장 변수
	pre_time = current_time		# 5초마다 'command' 전송을 위한 시각 변수

	time.sleep(0.5)		# 통신이 안정 될 때까지 잠깐 기다림


	#Ctrl+c가 눌릴 때까지 루프
	try:
		while True:
			# (A)화상 취득
			frame = drone.read()	# 영상 1프레임 획득
			if frame is None or frame.size == 0:	# 내용이 이상하면 무시
				continue 

			# (B)여기서 화상 처리
			image = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)		# OpenCV용 컬러와 함께 변환
			bgr_image = cv2.resize(image, dsize=(480,360) )	# 비디오 크기를 반으로 변경
			hsv_image = cv2.cvtColor(bgr_image, cv2.COLOR_BGR2HSV)	# BGR화상 -> HSV화상

			# (X)창에 표시
			cv2.imshow('BGR Color', bgr_image)	# 2개의 창을 만듬
			cv2.imshow('HSV Color', hsv_image)

			# (Y) OpenCV 창에서 키 입력을 1ms 기다리다
			key = cv2.waitKey(1)
			if key == 27:					# key가 27(ESC)이면 while 루프를 탈출, 프로그램 종료
				break
			elif key == ord('t'):
				drone.takeoff()				# 이륙
			elif key == ord('l'):
				drone.land()				# 착륙
			elif key == ord('w'):
				drone.move_forward(0.3)		# 전진
			elif key == ord('s'):
				drone.move_backward(0.3)	# 후진
			elif key == ord('a'):
				drone.move_left(0.3)		# 좌 이동
			elif key == ord('d'):
				drone.move_right(0.3)		# 우 이동
			elif key == ord('q'):
				drone.rotate_ccw(20)		# 좌 선회
			elif key == ord('e'):
				drone.rotate_cw(20)			# 우 선회
			elif key == ord('r'):
				drone.move_up(0.3)			# 상승
			elif key == ord('f'):
				drone.move_down(0.3)		# 하강
			# (Z)5초 간격으로 'command'를 보내어 이상 검사함
			current_time = time.time()	# 현재 시각 취득
			if current_time - pre_time > 5.0 :	# 전회 시각으로부터 5초 이상 경과하였는가?
				drone.send_command('command')	# 'command'송신
				pre_time = current_time			# 전회 시각 갱신
	except( KeyboardInterrupt, SystemExit):    # Ctrl+c누르면 이탈
		print( "SIGINTを検知" )

	# tello클래스 삭제
	del drone


# "python main.py"으로 실행되었을 때만 움직이게 하는 주술적 처리
if __name__ == "__main__":		# import시 '__main__'가 들어가지 않으므로 실행인지 import인지를 판단할 수 있다.
	main()    # 메인함수 실행