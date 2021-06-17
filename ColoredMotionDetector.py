#explaination:
#step1-first we will open webcam,and fetch first frame in a variable and convert it into gray image
#step2-then we will fetch next frame and convert into Gray and find the difference b/w first and current frame
#step3-we will see if diff is > 35 ,we will make that part White and rest as Black
#step4-these white parts are called as contours, we will find area of all contours.
#step5-if area of contour is > 1000, we will draw a rectangle on it.
#step6-now we will show datetime of object entry and exit
#step7-bokeh chart



import cv2 #image and video processing library
from datetime import datetime
import pandas
video=cv2.VideoCapture(0)  #opening webcam, here 0 means our webcam

first_frame=None
status_list=[None,None] #imp otherwise it will give error in line45-48
times=[] #it will store entering and exiting time of an object

df=pandas.DataFrame(columns=["Start","End"])


while True:
    check, frame=video.read() #making frame (capturing images)
    #print(check)
    #print(frame)
    status=0   #means no object entered

    gray_image=cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY) #converting to gray
    gray_image=cv2.GaussianBlur(gray_image,(21,21),0)  #converting to blurry images to get more accurate answers   (height=21,width=21)

    if first_frame is None:
        first_frame=gray_image #we are storing first image in first_frame variable
        continue   #using continue bcoz we need 1st frame only once

    delta_frame=cv2.absdiff(first_frame,gray_image)  #finding diff b/w first_frame and gray_image
    thresh_frame=cv2.threshold(delta_frame, 35, 255, cv2.THRESH_BINARY)[1] #here we are saying , give us only those parts of image which has Difference Greater than 35 , and make them White(255),,, and make rest part of image as Black
    thresh_frame=cv2.dilate(thresh_frame, None, iterations=2) #here we are removing unnecessary black spots that are present in our which portion,    more value of iteraion is good ,as it searches better

    (cnts,_)=cv2.findContours(thresh_frame.copy(),cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)  #finding contours      note= here we made a copy of thershold_frame ,so as to prevent errors

    for contour in cnts:
        if cv2.contourArea(contour)<10000:
            continue

        status=1  #means object entered
        
        (x,y,w,h)=cv2.boundingRect(contour) #here x,y,w,h will automatically find cordinates of that contour
        cv2.rectangle(frame, (x,y),(x+w,y+h), (0,255,0),3)   #making a green rectangle on that contour  #RBG

    status_list.append(status)


    if status_list[-1]==1 and status_list[-2]==0: #object entering
        times.append(datetime.now())
    if status_list[-1]==0 and status_list[-2]==1:  #object leaving
        times.append(datetime.now())

    cv2.imshow("myvideo",frame) #displaying on window
    cv2.imshow("deltaWindow",delta_frame) #displaying  difference frame on window
    cv2.imshow("thresh_window",thresh_frame)  #displaying contour frame on window
    key=cv2.waitKey(1)

    if key==ord('q'):
        if status==1: 
            times.append(datetime.now()) #it means if object is still present in window , and you closed web cam , then store time of that instance also
        break

#print(times)
for i in range(0,len(times),2):
    df=df.append({"Start":times[i], "End":times[i+1]},ignore_index=True)
#print(df)
df.to_csv("Times.csv") #converting into csv file
video.release() #closing webcam
cv2.destroyAllWindows()