#!/usr/bin/env python3
 # license removed for brevity
import rospy
from cv2 import cv2
import time
import datetime
from std_msgs.msg import String 
import csv
from datetime import datetime,date

def talker(data):
    pub = rospy.Publisher('chatter', String, queue_size=10)
    rospy.init_node('talker', anonymous=True)
    rate = rospy.Rate(10) # 10hz
    while not rospy.is_shutdown():
        hello_str = "Entered Hostel %s" % data
        rospy.loginfo(hello_str)
        pub.publish(hello_str)
        rate.sleep()
        break
# initalize the cam
cap = cv2.VideoCapture(0)
# initialize the cv2 QRCode detector
detector = cv2.QRCodeDetector()
#csv_file = "data.csv"
#csv_columns = ['name','reg_no', 'College','Hostel Block', 'Date','Time_Punched']
while True:
    _, img = cap.read()
    # detect and decode
    data, bbox, _ = detector.detectAndDecode(img)
    # check if there is a QRCode in the image
    if bbox is not None:
        # display the image with lines
        for i in range(len(bbox)):
            # draw all lines
            cv2.line(img, tuple(bbox[i][0]), tuple(bbox[(i+1) % len(bbox)][0]), color=(255, 0, 0), thickness=2)
        if data:
            print("[+] QR Code detected, data:", data)
          
            data_dict= list(data)
            now = datetime.now()
            Time_Punched= now.strftime("%H:%M:%S")
             
            
            #dict = {'name': data_dict[0], 'reg_number': data_dict[1], 'College': data_dict[2], 'Hostel Block': data_dict[3], 'Date': date, 'Time_Punched': Time_Punched }
            

            talker(data)
            time.sleep(2)
    # display the result
    cv2.imshow("img", img)    
    if cv2.waitKey(1) == ord("q"):
        break
cap.release()
cv2.destroyAllWindows()