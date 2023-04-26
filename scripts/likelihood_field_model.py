#!/usr/bin/python3
import rospy

import cv2
import numpy as np
from matplotlib import pyplot as plt
import math


if __name__=="__main__":
    # initialize this particle filter node
    rospy.init_node('likelihood')

    # Load the input image
    input_image = cv2.imread('map.png', cv2.IMREAD_GRAYSCALE)

    # Check if the input image was loaded successfully
    if input_image is None:
        print('Failed to load input image!')
        exit()
        
    # print(input_image)

    # Set the distance of black pixels to 0
    input_image[input_image == 205] = 0

    _ret, img2 = cv2.threshold(input_image, 0, 255, cv2.THRESH_BINARY)

    # kernel = np.ones((3, 3), np.uint8)
    # opn = cv2.morphologyEx(img2, cv2.MORPH_OPEN, kernel)
    distance = cv2.distanceTransform(img2, cv2.DIST_L2, 5)
    # _ret, result = cv2.threshold(distance, 0.7 * distance.max(), 255, cv2.THRESH_BINARY)

    print('dist[100][100]', distance[100][100])
    print('dist2[100][100]', (distance*distance)[100][100])
    print('dist[1][1]', distance[1][1])
    print('dist2[1][1]', (distance*distance)[1][1])
    # pprint.pprint('dist', distance[100][100])
    # pprint.pprint('dist2', (distance*distance)[100][100], width=1000)

    sigma_hit = 2
    z_hit = 1/pow(2*math.pi, 0.5)/sigma_hit # 0.5
    print('z_hit', z_hit)
    z_hit_denom = 2 * sigma_hit * sigma_hit

    # like_lihood = z_hit * np.exp(-(distance * distance)/z_hit_denom)*255
    like_lihood = np.exp(-(distance * distance)/z_hit_denom)*255

    print('like_lihood[100][100]', like_lihood[100][100])
    print('like_lihood[1][1]', like_lihood[1][1])



    plt.subplot(141), plt.imshow(input_image, cmap='gray'), plt.title('org'), plt.axis('off')
    plt.subplot(142), plt.imshow(img2, cmap='gray'), plt.title('img2'), plt.axis('off')
    # plt.subplot(143), plt.imshow(opn, cmap='gray'), plt.title('opn'), plt.axis('off')
    plt.subplot(143), plt.imshow(distance, cmap='gray'), plt.title('distance'), plt.axis('off')
    plt.subplot(144), plt.imshow(like_lihood, cmap='gray'), plt.title('like_lihood'), plt.axis('off')
    plt.show()

    # # Compute the distance transform of the input image
    # distance_transform = cv2.distanceTransform(input_image, cv2.DIST_L2, cv2.DIST_MASK_PRECISE)

    # # Normalize the distance transform to get the likelihood field
    # likelihood_field = cv2.normalize(distance_transform, None, 0, 255, cv2.NORM_MINMAX, cv2.CV_8UC1)

    # # Save the likelihood field image
    cv2.imwrite('distance.png', distance)
    cv2.imwrite('likelihood_field.png', like_lihood)


    rospy.spin()
