#importing libraries
import numpy as np
import cv2

#image stitch coordinator
def pano_bridge():
    # for 160* 
    pano('pics/1.jpg','pics/2.jpg','pics/pTemp.jpg')
    pano('pics/pTemp.jpg','pics/3.jpg','pics/pFinal.jpg')
    
    # for 360*
    #....dev in prog....

#panorama generator
def pano(dir1,dir2,fName):
   
    #read two pictures
    imageR = cv2.imread(dir1)
    grayR = cv2.cvtColor(imageR, cv2.COLOR_BGR2GRAY)
    imageL = cv2.imread(dir2)
    grayL = cv2.cvtColor(imageL, cv2.COLOR_BGR2GRAY)
    
    
    #detecting two image key points and feature description
    sift = cv2.SIFT_create()
    kp1, des1 = sift.detectAndCompute(grayL, None)
    kp2, des2 = sift.detectAndCompute(grayR, None)
    
    #making a match
    matcher = cv2.BFMatcher(cv2.NORM_L2)
    #knn match 
    rawMatcher = matcher.knnMatch(des1, des2, 2)
    
    #processing the matched feature points
    matchersTrain = []
    matchersQuery = []
    for matchA, matchB in rawMatcher:
        #arrange the distance between the two matches from small to large
        if matchA.distance < matchB.distance*0.75:
            #save the position of two points in des
            matchersTrain.append(matchA.trainIdx)
            matchersQuery.append(matchA.queryIdx)
            
    H = 0
    
    #calculating the transformation matrix after obtaining > 4 coordinates
    if len(matchersTrain) > 4:
        #getting a list of key points
        locL = np.float32([kp1[i].pt for i in matchersQuery])
        locR = np.float32([kp2[i].pt for i in matchersTrain])
        H, status = cv2.findHomography(locR, locL, cv2.RANSAC)

    else:
        print("Not enough points were found to match")
        
    #transform the image on the right
         
    change = cv2.warpPerspective(imageR, H, (imageL.shape[1] + imageR.shape[1], imageL.shape[0]))
        


    #combining the pics
    change[0:imageL.shape[0], 0:imageL.shape[1]] = imageL

    #panorama genertation  
    cv2.imwrite(fName,change)
    
    cv2.waitKey(0)
