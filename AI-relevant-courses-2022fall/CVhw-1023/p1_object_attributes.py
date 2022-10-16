#!/usr/bin/env python3
import cv2
import numpy as np
import sys
import math


def binarize(gray_image, thresh_val):
    # TODO: 255 if intensity >= thresh_val else 0
    binary_image = np.zeros(gray_image.shape, dtype='uint8')
    binary_image[gray_image >= thresh_val] = 255
    return binary_image


def label(binary_image):
    """
    Note that this method always assume that the pixels in the first row and first column are backgrounds
    for code simplicity. Since this is a computer vision task which processes actual images, this method
    assume that the information on the edges of the image is not important, hence can be omitted
    """
    # global variables
    parent = [0]  # for union-find operation
    num_types = 0  # number of types during the first pass
    inf = int(1e10)  # denote the regions where are backgrounds, for simplicity of codes
    height, width = binary_image.shape[0], binary_image.shape[1]

    # initialization
    labeled_img = np.ones(binary_image.shape, dtype='int') * inf

    # first pass
    for i in range(height-1):
        for j in range(width-1):
            if binary_image[i+1][j+1] == 0:
                labeled_img[i + 1][j + 1] = inf
            else:
                neighbour_type = min(labeled_img[i][j], labeled_img[i][j+1], labeled_img[i+1][j])
                if neighbour_type == inf:
                    num_types += 1
                    parent.append(num_types)
                    labeled_img[i + 1][j + 1] = num_types
                else:
                    labeled_img[i + 1][j + 1] = neighbour_type
                    if labeled_img[i][j] < inf:
                        parent[labeled_img[i][j]] = min(neighbour_type, parent[labeled_img[i][j]])
                    if labeled_img[i+1][j] < inf:
                        parent[labeled_img[i+1][j]] = min(neighbour_type, parent[labeled_img[i+1][j]])
                    if labeled_img[i][j+1] < inf:
                        parent[labeled_img[i][j+1]] = min(neighbour_type, parent[labeled_img[i][j+1]])

    # union find set
    for i in range(len(parent)):
        p = parent[i]
        while p != parent[p]:
            p = parent[p]
        parent[i] = p

    # second pass
    types = set(parent)
    types.discard(0)
    for i in range(len(parent)):
        labeled_img[labeled_img == i] = parent[i]
    curr_cc = 0
    labeled_img[labeled_img == inf] = 0  # background
    for elem in types:
        curr_cc += 1
        labeled_img[labeled_img == elem] = int(255 * curr_cc / len(types))
    return labeled_img


def get_attribute(labeled_image):
    # initialization
    types = set(np.unique(labeled_image))
    types.discard(0)
    att_list = []
    height, width = labeled_image.shape[0], labeled_image.shape[1]

    def calculate_E(theta, a, b, c):
        return a * math.sin(theta) ** 2 - b * math.sin(theta) * math.cos(theta) + c * math.cos(theta) ** 2

    # tackle these objects one at a time
    for elem in types:
        # generate image with single object each time
        obj_img = np.zeros(labeled_image.shape, dtype='uint8')
        obj_img[labeled_image == elem] = 1
        parameters = {'position': {'x': 0, 'y': 0}, 'orientation': 0, 'roundedness': 0}

        # calculate the position
        area = np.sum(obj_img)
        x, y = np.arange(width).reshape(1, -1), height - np.arange(height).reshape(height, -1)
        x_bar, y_bar = np.sum(obj_img * x)/area, np.sum(obj_img * y)/area
        parameters['position']['x'], parameters['position']['y'] = x_bar, y_bar

        # calculate the orientation and roundedness
        x_prime, y_prime = x - x_bar, y - y_bar
        a, b, c = np.sum(x_prime ** 2 * obj_img), 2 * np.sum(x_prime * y_prime * obj_img),\
                  np.sum(y_prime ** 2 * obj_img)
        theta1 = math.atan(b / (a - c)) / 2
        theta2 = theta1 + math.pi/2
        e1, e2 = calculate_E(theta1, a, b, c), calculate_E(theta2, a, b, c)
        if e1 < e2:
            parameters['orientation'], parameters['roundedness'] = theta1, e1/e2
        else:
            parameters['orientation'], parameters['roundedness'] = theta2, e2/e1
        att_list.append(parameters)
    return att_list


def main(argv):
    img_name = argv[0]
    thresh_val = int(argv[1])
    img = cv2.imread('data/' + img_name + '.png', cv2.IMREAD_COLOR)
    gray_image = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    binary_image = binarize(gray_image, thresh_val=thresh_val)
    labeled_image = label(binary_image)

    attribute_list = get_attribute(labeled_image)

    cv2.imwrite('output/' + img_name + "_gray.png", gray_image)
    cv2.imwrite('output/' + img_name + "_binary.png", binary_image)
    cv2.imwrite('output/' + img_name + "_labeled.png", labeled_image)

    print(attribute_list)


if __name__ == '__main__':
    main(sys.argv[1:])
