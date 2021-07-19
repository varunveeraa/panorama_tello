#importing libraries
from djitellopy import tello
import keyboard as key
from time import sleep
from pano import pano_bridge
import cv2

#initiating communication
drone = tello.Tello()
drone.connect()
drone.streamon()

print(drone.get_battery())

#manual override
def getInput():
    lr, fb, ud, yv = 0, 0, 0, 0
    x = 60 
    #key press detection
    if key.is_pressed('left'): 
        lr = -x
    elif key.is_pressed('right'): 
        lr = x
    
    if key.is_pressed('up'): 
        ud = x
    elif key.is_pressed('down'): 
        ud = -x
    
    if key.is_pressed('w'): 
        fb = x
    elif key.is_pressed("s"): 
        fb = -x
    
    if key.is_pressed('a'): 
        yv = -x
    elif key.is_pressed('d'): 
        yv = x
        
    if key.is_pressed('t'):  
        drone.takeoff()
    elif key.is_pressed('l'): 
        drone.land()
        
        
    return [lr, fb, ud, yv]

#image capture movements
def right():
    drone.send_rc_control(0,0,0,35)
    sleep(2)
    ntg()
     
def left():
    drone.send_rc_control(0,0,0,-35)
    sleep(2)
    ntg()
    
def ntg():
    drone.send_rc_control(0,0,0,0)
    sleep(1)
    
#capturing images
def capture(i):
    cap = drone.get_frame_read().frame
    loc1 = 'F:/Projects/droneProj/v2.0/Pano/Pics/'+str(i)+'.jpg'
    cv2.imwrite(loc1, cap)
    
def panorama():
    #image capture begin
    ntg()
    right()
    capture(1)
    left()
    capture(2)
    left()
    capture(3)
    right()
    ntg()
    
    #image stitch' processing
    pano_bridge()
    
def features():
    if key.is_pressed('P'):
        panorama()

while True:
    #manual controls
    val = getInput()
    drone.send_rc_control(val[0], val[1], val[2], val[3])
    
    #feature detection
    features()
    
    #get frames from tello
    frame = drone.get_frame_read().frame
    
    #output live relay
    cv2.imshow("Live Stream", frame)
    cv2.waitKey(1)
