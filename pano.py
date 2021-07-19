import cv2 as cv
import numpy as np

def pano_bridge():
    # for 160* 
    pano('pics/1.jpg','pics/2.jpg','pics/pTemp.jpg')
    pano('pics/pTemp.jpg','pics/3.jpg','pics/pFinal.jpg')
    
    # for 360*
    #....dev in prog....

def pano(dir1,dir2,dirN):
   
    # Read two pictures
    imageR = cv.imread(dir1)
    grayR = cv.cvtColor(imageR, cv.COLOR_BGR2GRAY)
    imageL = cv.imread(dir2)
    grayL = cv.cvtColor(imageL, cv.COLOR_BGR2GRAY)
    
    
    # Detect two image key points and feature description factors
    sift = cv.SIFT_create()
    kp1, des1 = sift.detectAndCompute(grayL, None)
    kp2, des2 = sift.detectAndCompute(grayR, None)
    
    # Make a match
    matcher = cv.BFMatcher(cv.NORM_L2)
    # k'n'nmatch 
    rawMatcher = matcher.knnMatch(des1, des2, 2)
    
    # Process the matched feature points
    matchersTrain = []
    matchersQuery = []
    for matchA, matchB in rawMatcher:
        # Arrange the distance between the two matches from small to large
        if matchA.distance < matchB.distance*0.75:
            # Save the position of two points in des
            matchersTrain.append(matchA.trainIdx)
            matchersQuery.append(matchA.queryIdx)
            
    H = 0
    # Calculate the transformation matrix after obtaining more than 4 coordinates
    if len(matchersTrain) > 4:
        # Get a list of key points
        locL = np.float32([kp1[i].pt for i in matchersQuery])
        locR = np.float32([kp2[i].pt for i in matchersTrain])
        H, status = cv.findHomography(locR, locL, cv.RANSAC)

    else:
        print("Not enough points were found to match")
        
    # Transform the image on the right
         
    change = cv.warpPerspective(imageR, H, (imageL.shape[1] + imageR.shape[1], imageL.shape[0]))
        


    # Combine pictures
    change[0:imageL.shape[0], 0:imageL.shape[1]] = imageL

    # Save original image 
    cv.imwrite(dirN,change)
    
    cv.waitKey(0)
