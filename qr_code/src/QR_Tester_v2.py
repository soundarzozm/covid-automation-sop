
# Required to install: OpenCV Python, Numpy, Pyzbar

from __future__ import print_function

import pyzbar.pyzbar as pyzbar
import numpy as np
from cv2 import cv2
import time
import rospy
from std_msgs.msg import String 

def talker(data):
    pub = rospy.Publisher('chatter', String, queue_size=10)
    rospy.init_node('talker', anonymous=True)
    rate = rospy.Rate(60) # 10hz
    while not rospy.is_shutdown():
        hello_str = "Entered Hostel %s" % data
        rospy.loginfo(hello_str)
        pub.publish(hello_str)
        rate.sleep()
        break

# Get the Webcam:  
cap = cv2.VideoCapture(0) # If Using In-built webcam try changing 1 to 0 Here

cap.set(3,640)
cap.set(4,480)

time.sleep(2)

def decode(im) : 
    # Find barcodes and QR codes
    decodedObjects = pyzbar.decode(im)
    # Print results
#    for obj in decodedObjects:
#        print('Type : ', obj.type)
#        print('Data : ', obj.data,'\n')     
    return decodedObjects


font = cv2.FONT_HERSHEY_SIMPLEX

while(cap.isOpened()):
    # Capture frame-by-frame
    ret, frame = cap.read()
    # Our operations on the frame come here
    im = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
         
    decodedObjects = decode(im)

    for decodedObject in decodedObjects: 
        points = decodedObject.polygon
     
        # If the points do not form a quad, find convex hull
        if len(points) > 4 : 
          hull = cv2.convexHull(np.array([point for point in points], dtype=np.float32))
          hull = list(map(tuple, np.squeeze(hull)))
        else : 
          hull = points
         
        # Number of points in the convex hull
        n = len(hull)     
        # Draw the convext hull
        for j in range(0,n):
          cv2.line(frame, hull[j], hull[ (j+1) % n], (255,0,0), 3)

        x = decodedObject.rect.left
        y = decodedObject.rect.top

        # print(x, y)


        barCode = str(decodedObject.data)
        overlay1 = barCode.replace("b\'","")
        overlay2 = overlay1.replace("\'","")

        print('Data Detected, Type : ', decodedObject.type)
        print('Data : ', overlay2,'\n')
        talker(overlay2)

        cv2.putText(frame, overlay2, (x, y), font, 1, (0,0,255), 2, cv2.LINE_AA)
               
    # Display the resulting frame
    cv2.imshow('frame',frame)
    key = cv2.waitKey(1)
    if key & 0xFF == ord('q'):
        break
    elif key & 0xFF == ord('s'): # wait for 's' key to save 
        cv2.imwrite('Last_QR_Saved.png', frame)     

# When everything done, release the capture
cap.release()
cv2.destroyAllWindows()
