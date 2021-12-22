import cv2

baseline_image=None
status_list=[None,None]
video=cv2.VideoCapture(0)

while True:
    check, frame = video.read()
    if frame is None: 
        print("empty frame")
        exit(1)
    status=0
    gray_frame=cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)
    gray_frame=cv2.GaussianBlur(gray_frame,(25,25),0)

    if baseline_image is None:
        baseline_image=gray_frame
        continue

    delta=cv2.absdiff(baseline_image,gray_frame)
    threshold=cv2.threshold(delta, 30, 255, cv2.THRESH_BINARY)[1]
    (contours,_)=cv2.findContours(threshold,cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    for contour in contours:
        if cv2.contourArea(contour) < 10000:
            continue

        status=1
        (x, y, w, h)=cv2.boundingRect(contour)
        print(str(w*h))
        cv2.rectangle(frame, (x, y), (x+w, y+h), (0,255,0), 1)
        status_list.append(status)
	

    #cv2.imshow("gray_frame Frame",gray_frame)
    #cv2.imshow("Delta Frame",delta)
    #cv2.imshow("Threshold Frame",threshold)
    cv2.imshow("Color Frame",frame)

    key=cv2.waitKey(1)

    if key==ord('q'):
        break


#Clean up, Free memory
engine.stop()
video.release()
cv2.destroyAllWindows

