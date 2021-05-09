
# Required to install: OpenCV Python, Numpy, Pyzbar, ROS

from __future__ import print_function

from pyzbar import pyzbar
import numpy as np
from cv2 import cv2
import rospy
import time
from datetime import datetime
from std_msgs.msg import String 
from datetime import date 
import csv


def talker(data):
    pub = rospy.Publisher('chatter', String, queue_size=30)
    rospy.init_node('talker', anonymous=True)
    rate = rospy.Rate(1) # 1Hz
    while not rospy.is_shutdown():
        ToPub1 = "Entered Hostel: %s" % data
        ToPub2 = ToPub1 + " On " + date.today() + " At " + datetime.now().strftime("%H:%M:%S")
        rospy.loginfo(ToPub2)
        pub.publish(ToPub2)
        rate.sleep()
        break


# Get the Webcam:  
cap = cv2.VideoCapture(0) # If Using In-built webcam try changing 1 to 0 Here
csv_file = "data.csv"
csv_columns = ['name','reg_no', 'College','Hostel Block', 'Date','Time_Punched']
cap.set(3,640)
cap.set(4,480)

time.sleep(2)

def decode(im) : 
    # Find barcodes and QR codes
    decodedObjects = pyzbar.decode(im)
    # Print results
    for obj in decodedObjects:
        print('Type : ', obj.type)
        print('Data : ', obj.data,'\n')     
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

        print(x, y)

        print('Type : ', decodedObject.type)
        print('Data : ', decodedObject.data,'\n')

        barCode = str(decodedObject.data)
        overlay1 = barCode.replace("b\'","")
        overlay2 = overlay1.replace("\'","")
        cv2.putText(frame, overlay2, (x, y), font, 1, (0,0,255), 2, cv2.LINE_AA)
        data_dict= list(decodedObject.data)
        now = datetime.now()
        Time_Punched= now.strftime("%H:%M:%S")
        dict = {'name': data_dict[0], 'reg_number': data_dict[1], 'College': data_dict[2], 'Hostel Block': data_dict[3], 'Date': date, 'Time_Punched': Time_Punched }
        try:
            with open(csv_file, 'w') as csvfile:
                writer = csv.DictWriter(csvfile, fieldnames=csv_columns)
                writer.writeheader()
                for data in dict:
                        writer.writerow(data)
        except IOError:
                print("I/O error")
        talker(overlay2)
               
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
